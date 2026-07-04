const express = require("express");
const axios = require("axios");
const config = require("../config");
const { validateTagRequest } = require("../middleware/validator");
const apiLimiter = require("../middleware/rateLimiter");

const router = express.Router();

/**
 * POST /api/tag
 * Proxies the request to the FastAPI backend
 */
router.post("/tag", apiLimiter, validateTagRequest, async (req, res) => {
  try {
    const { text, max_tags } = req.body;
    
    // Call FastAPI backend
    const response = await axios.post(`${config.fastapiUrl}/analyze`, {
      text: text,
      max_tags: max_tags || 5
    });

    // Send successful response to client
    return res.status(200).json({
      success: true,
      data: response.data,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    // Handle Axios errors (FastAPI returned 4xx or 5xx)
    if (error.response) {
      return res.status(error.response.status).json({
        success: false,
        error: error.response.data.detail || "Error from AI Backend"
      });
    }
    
    // Handle network/other errors
    console.error("Express Proxy Error:", error.message);
    return res.status(500).json({
      success: false,
      error: "Internal Server Error — Could not reach AI Backend"
    });
  }
});

module.exports = router;
