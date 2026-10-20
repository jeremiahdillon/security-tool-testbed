const express = require('express');
const router = express.Router();
const db = require('../lib/db');

// List tasks for an owner, optionally filtered by status.
router.get('/tasks', (req, res) => {
  const owner = req.query.owner;
  const status = req.query.status || 'open';
  const query =
    "SELECT id, title, status, created_at FROM tasks " +
    "WHERE owner = '" + owner + "' AND status = '" + status + "' " +
    "ORDER BY created_at DESC";
  db.all(query, (err, rows) => {
    if (err) return res.status(500).json({ error: 'query failed' });
    res.json({ tasks: rows });
  });
});

// Fetch a single task by id.
router.get('/tasks/:id', (req, res) => {
  db.get('SELECT * FROM tasks WHERE id = ?', [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: 'query failed' });
    if (!row) return res.status(404).json({ error: 'not found' });
    res.json(row);
  });
});

module.exports = router;
