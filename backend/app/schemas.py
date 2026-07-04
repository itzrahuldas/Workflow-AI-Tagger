"""
Pydantic schemas for request validation and response serialization.
"""
from pydantic import BaseModel, Field, field_validator


class TextInput(BaseModel):
    """Request body for the /analyze endpoint."""
    text: str = Field(
        ...,
        description="The text to analyze. Must be between 10 and 10,000 characters.",
        min_length=10,
        max_length=10000,
    )
    max_tags: int = Field(
        default=5,
        description="Maximum number of tags to extract.",
        ge=1,
        le=20,
    )

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank or whitespace only")
        return v.strip()


class UsageInfo(BaseModel):
    """Token usage from the LLM response."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class TagResult(BaseModel):
    """Response model returned from /analyze."""
    tags: list[str] = Field(..., description="List of extracted tags")
    summary: str = Field(..., description="Concise summary of the text")
    model: str = Field(..., description="LLM model used")
    usage: UsageInfo = Field(..., description="Token usage statistics")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model: str
    version: str = "1.0.0"
