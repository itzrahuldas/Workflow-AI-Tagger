const morgan = require("morgan");

/**
 * Request logger using Morgan.
 * Customize the format to include timestamp, method, url, status, and response time.
 */
const logger = morgan(
  ":date[iso] | :method :url | Status: :status | :response-time ms",
  {
    skip: (req, res) => req.url === "/health", // Don't spam logs with health checks
  }
);

module.exports = logger;
