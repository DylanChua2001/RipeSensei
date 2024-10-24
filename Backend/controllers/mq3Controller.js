// controllers/mq3Controller.js
const { getMQ3Data } = require("../models/mq3Model");

const fetchMQ3Data = async (req, res) => {
  try {
    const data = await getMQ3Data();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = { fetchMQ3Data };
