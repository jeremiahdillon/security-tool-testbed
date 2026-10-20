const sqlite3 = require('sqlite3');
const config = require('./config');

// Thin wrapper around a sqlite3 connection used across the API.
const db = new sqlite3.Database(config.db.path);

module.exports = db;
