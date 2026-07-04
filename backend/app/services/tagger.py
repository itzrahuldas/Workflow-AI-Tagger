"""
Tagger Service — Core AI logic using Groq API with OpenAI function calling.

Groq is OpenAI-compatible, so we use the openai SDK pointed at Groq's base URL.
Function calling forces the LLM to return a strict JSON schema every time.
"""
import json
import logging
from openai import AsyncOpenAI

from app.config import Settings
from app.schemas import TagResult, UsageInfo

logger = logging.getLogger(__name__)

# ── Function definition for OpenAI / Groq function calling ───────────────────
EXTRACT_FUNCTION = {
    "name": "extract_tags_and_summary",
    "description": (
        "Extract the most relevant tags and a concise summary from the provided text. "
        "Tags should be lowercase, specific keywords or key phrases."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of lowercase keywords/key-phrases that best represent the text topics.",
            },
            "summary": {
                "type": "string",
                "description": (
                    "A concise 1–3 sentence summary capturing the core meaning of the text."
                ),
            },
        },
        "required": ["tags", "summary"],
    },
}


class TaggerService:
    """Service that calls Groq LLM and returns structured TagResult."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        # Groq is 100% OpenAI-SDK-compatible — just swap the base_url
        self._client = AsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
        )

    async def tag(self, text: str, max_tags: int = 5) -> TagResult:
        """
        Send text to the LLM via function calling.
        Returns a fully validated TagResult.
        """
        system_prompt = (
            "You are an expert text analyst. "
            "When given a text, you extract precise, relevant tags and write a clear summary. "
            f"Extract at most {max_tags} tags. "
            "Always call the extract_tags_and_summary function with your result."
        )

        logger.info(
            f"🤖 Calling Groq [{self._settings.model_name}] "
            f"| text_len={len(text)} | max_tags={max_tags}"
        )

        response = await self._client.chat.completions.create(
            model=self._settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze the following text:\n\n{text}"},
            ],
            tools=[{"type": "function", "function": EXTRACT_FUNCTION}],
            # Force the model to always call our function — no free-text fallback
            tool_choice={"type": "function", "function": {"name": "extract_tags_and_summary"}},
            max_tokens=self._settings.max_tokens,
            temperature=0.3,  # lower temp = more deterministic/structured output
        )

        # ── Parse function call result ────────────────────────────────────────
        message = response.choices[0].message
        tool_calls = message.tool_calls

        if not tool_calls:
            raise ValueError(
                "LLM did not return a function call. "
                "This is unexpected — check your API key and model name."
            )

        raw_args = tool_calls[0].function.arguments
        logger.debug(f"📦 Raw function args: {raw_args}")

        try:
            parsed = json.loads(raw_args)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM function call response as JSON: {e}")

        # Validate required fields
        if "tags" not in parsed or "summary" not in parsed:
            raise ValueError(
                f"LLM response missing required fields. Got: {list(parsed.keys())}"
            )

        # Enforce max_tags cap (safety net)
        tags = parsed["tags"][:max_tags]

        # ── Build response ────────────────────────────────────────────────────
        usage = response.usage
        return TagResult(
            tags=tags,
            summary=parsed["summary"],
            model=response.model,
            usage=UsageInfo(
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
            ),
        )
