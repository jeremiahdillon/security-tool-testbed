const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const path = require('path');

const UPLOAD_DIR = '/var/taskflow/uploads';
const THUMB_DIR = '/var/taskflow/thumbs';

// Generate a thumbnail for an uploaded image attachment.
router.post('/attachments/:name/thumbnail', (req, res) => {
  const name = req.params.name;
  const src = path.join(UPLOAD_DIR, name);
  const dst = path.join(THUMB_DIR, name);
  const cmd = `convert ${src} -resize 128x128 ${dst}`;
  exec(cmd, (err) => {
    if (err) return res.status(500).json({ error: 'thumbnail failed' });
    res.json({ thumbnail: dst });
  });
});

module.exports = router;
