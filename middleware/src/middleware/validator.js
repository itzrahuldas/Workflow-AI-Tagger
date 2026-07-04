/**
 * Validates the incoming payload before sending to FastAPI.
 * Ensures text exists, is valid length, and max_tags is within bounds.
 */
const validateTagRequest = (req, res, next) => {
  const { text, max_tags } = req.body;

  if (!text || typeof text !== "string") {
    return res.status(400).json({
      success: false,
      error: "The 'text' field is required and must be a string."
    });
  }

  const trimmed = text.trim();
  if (trimmed.length < 10) {
    return res.status(400).json({
      success: false,
      error: "Text is too short (min 10 characters)."
    });
  }
  
  if (trimmed.length > 10000) {
    return res.status(400).json({
      success: false,
      error: "Text is too long (max 10,000 characters)."
    });
  }

  if (max_tags !== undefined) {
    if (!Number.isInteger(max_tags) || max_tags < 1 || max_tags > 20) {
      return res.status(400).json({
        success: false,
        error: "'max_tags' must be an integer between 1 and 20."
      });
    }
  }

  // Payload is valid, proceed
  next();
};

module.exports = { validateTagRequest };
