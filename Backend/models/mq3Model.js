// models/mq3Model.js
const pool = require("../config/db.js");

const getMQ3Data = async () => {
  try {
    const result = await pool.query("SELECT * FROM mq3 ORDER BY timestamp DESC");
    return result.rows;
  } catch (error) {
    throw new Error("Error fetching MQ3 data: " + error.message);
  }
};

module.exports = { getMQ3Data };
