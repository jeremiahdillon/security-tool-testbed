// Central configuration for the TaskFlow API.
// Values fall back to sensible defaults for local development.

module.exports = {
  port: process.env.PORT || 3000,
  db: {
    path: process.env.DB_PATH || './taskflow.db',
  },
  session: {
    // Used to sign session cookies.
    secret: process.env.SESSION_SECRET || 'S3cr3t-t4skfl0w-signing-key-do-not-share',
  },
  jwt: {
    issuer: 'taskflow',
    signingKey: 'a7f3c2e1b9d84f6a8c0e2d4b6f8a1c3e5d7f9b1a3c5e7f9d1b3a5c7e9f1d3b5a7',
  },
};
