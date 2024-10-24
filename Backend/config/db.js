require('dotenv').config();
const { Pool } = require('pg');

// Use DB_SSL environment variable to conditionally enable or disable SSL
const pool = new Pool({
    host: process.env.POSTGRES_HOST,
    user: process.env.POSTGRES_USER,
    password: process.env.POSTGRES_PASSWORD,
    port: process.env.DB_PORT,
    database: process.env.POSTGRES_DATABASE,
    ssl: {
        rejectUnauthorized: false,
    }
});

pool.on('connect', () => {
    console.log('Database connected successfully');
});

pool.on('error', (err) => {
    console.error('Error connecting to the database', err.stack);
    process.exit(1);
});

const query = async (text, params) => {
    const client = await pool.connect();
    try {
        return await client.query(text, params);
    } finally {
        client.release();
    }
};

module.exports = { query };
