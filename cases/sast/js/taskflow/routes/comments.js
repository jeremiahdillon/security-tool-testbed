const express = require('express');
const router = express.Router();
const db = require('../lib/db');
const { requireUser } = require('../lib/auth');

// List the comments on one of the caller's tasks.
router.get('/tasks/:taskId/comments', requireUser, (req, res) => {
  db.get('SELECT owner FROM tasks WHERE id = ?', [req.params.taskId], (err, task) => {
    if (err) return res.status(500).json({ error: 'query failed' });
    if (!task || task.owner !== req.user.id) return res.status(404).json({ error: 'not found' });
    db.all(
      'SELECT id, author, body, created_at FROM comments WHERE task_id = ? ORDER BY created_at',
      [req.params.taskId],
      (err2, rows) => {
        if (err2) return res.status(500).json({ error: 'query failed' });
        res.json({ comments: rows });
      }
    );
  });
});

// Edit the text of a comment.
router.put('/comments/:id', requireUser, (req, res) => {
  const body = String(req.body.body || '').trim();
  if (!body) return res.status(400).json({ error: 'body is required' });
  db.run('UPDATE comments SET body = ? WHERE id = ?', [body, req.params.id], function (err) {
    if (err) return res.status(500).json({ error: 'update failed' });
    if (this.changes === 0) return res.status(404).json({ error: 'not found' });
    res.json({ id: Number(req.params.id), body });
  });
});

// Remove a comment.
router.delete('/comments/:id', requireUser, (req, res) => {
  db.run(
    'DELETE FROM comments WHERE id = ? AND author = ?',
    [req.params.id, req.user.id],
    function (err) {
      if (err) return res.status(500).json({ error: 'delete failed' });
      if (this.changes === 0) return res.status(404).json({ error: 'not found' });
      res.status(204).end();
    }
  );
});

module.exports = router;
