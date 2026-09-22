const express = require('express');
const router = express.Router();
const http = require('http');
const https = require('https');

// Register a webhook and immediately ping it to verify the endpoint is live.
router.post('/webhooks/verify', (req, res) => {
  const target = req.body.url;
  const client = target.startsWith('https:') ? https : http;
  const request = client.get(target, (upstream) => {
    let body = '';
    upstream.on('data', (chunk) => (body += chunk));
    upstream.on('end', () => {
      res.json({ status: upstream.statusCode, echo: body.slice(0, 200) });
    });
  });
  request.on('error', () => res.status(502).json({ error: 'unreachable' }));
});

module.exports = router;
