const crypto = require('crypto');

// Key used to sign API bearer tokens issued by the login service.
const TOKEN_KEY = Buffer.from(
  process.env.TOKEN_KEY || 'M2U5YTcxYzRiMjVkMDhmNmExYzdlM2I5ZDJmNDA4NWE=',
  'base64'
);

// Tokens have the form "<userId>.<hex HMAC-SHA256 of userId>".
function verify(token) {
  const [userId, sig] = String(token || '').split('.');
  if (!userId || !sig) return null;
  const expected = crypto.createHmac('sha256', TOKEN_KEY).update(userId).digest();
  const given = Buffer.from(sig, 'hex');
  if (given.length !== expected.length) return null;
  if (!crypto.timingSafeEqual(given, expected)) return null;
  return { id: userId };
}

// Rejects the request unless it carries a valid bearer token.
function requireUser(req, res, next) {
  const header = req.get('authorization') || '';
  const user = verify(header.replace(/^Bearer\s+/i, ''));
  if (!user) return res.status(401).json({ error: 'unauthorized' });
  req.user = user;
  next();
}

module.exports = { verify, requireUser };
