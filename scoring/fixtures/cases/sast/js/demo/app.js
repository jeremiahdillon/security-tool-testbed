const express = require('express');
const router = express.Router();
const db = require('../db');

router.get('/tasks', (req, res) => {
  const owner = req.query.owner;
  const query = `SELECT * FROM tasks WHERE owner = '${owner}'`;
  db.all(query, (err, rows) => {
    if (err) return res.status(500).send('error');
    res.json(rows);
  });
});

module.exports = router;
