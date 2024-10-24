// index.js
const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const mq3Routes = require("./routes/mq3Route");

dotenv.config();
const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Use the mq3 routes
app.use("/api", mq3Routes);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
