const rateLimit = require("express-rate-limit");
const config = require("../config");

/**
 * Rate limiter middleware to protect the proxy/AI endpoint.
 */
const apiLimiter = rateLimit({
  windowMs: config.rateLimit.windowMs, // default 15 mins
  max: config.rateLimit.max,           // default 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: "Too many requests from this IP, please try again later."
  }
});

module.exports = apiLimiter;
