const express = require('express');
const config = require('./lib/config');

const tasks = require('./routes/tasks');
const attachments = require('./routes/attachments');
const webhooks = require('./routes/webhooks');

const app = express();
app.use(express.json());
app.use('/api', tasks);
app.use('/api', attachments);
app.use('/api', webhooks);

app.listen(config.port, () => {
  console.log(`TaskFlow API listening on ${config.port}`);
});
