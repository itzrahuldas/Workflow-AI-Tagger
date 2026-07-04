const express = require("express");
const cors = require("cors");
const config = require("./config");
const logger = require("./middleware/logger");
const tagRoutes = require("./routes/tagRoutes");

const app = express();

// ── Middleware ─────────────────────────────────────────────────────────────
app.use(cors());                 // Enable CORS for all routes
app.use(express.json());         // Parse JSON bodies
app.use(logger);                 // Log requests

// ── Routes ─────────────────────────────────────────────────────────────────
app.use("/api", tagRoutes);

// Health check endpoint (for Docker/orchestration)
app.get("/health", (req, res) => {
  res.status(200).json({ 
    service: "middleware", 
    status: "healthy",
    target: config.fastapiUrl
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ success: false, error: "Route not found" });
});

// ── Server Start ───────────────────────────────────────────────────────────
app.listen(config.port, () => {
  console.log(`🚀 Express Middleware running on port ${config.port}`);
  console.log(`🔗 Proxying AI requests to ${config.fastapiUrl}`);
});
