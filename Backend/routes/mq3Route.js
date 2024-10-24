// routes/mq3Routes.js
const express = require("express");
const { fetchMQ3Data } = require("../controllers/mq3Controller");
const router = express.Router();

// Route to fetch all MQ3 sensor data
router.get("/mq3data", fetchMQ3Data);

module.exports = router;
