/**
 * config.js — Load and export all middleware configuration from .env
 */
require("dotenv").config();

module.exports = {
  port: parseInt(process.env.PORT || "3000", 10),
  fastapiUrl: process.env.FASTAPI_URL || "http://localhost:8000",
  rateLimit: {
    max: parseInt(process.env.RATE_LIMIT_MAX || "100", 10),
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || "900000", 10),
  },
  nodeEnv: process.env.NODE_ENV || "development",
};
