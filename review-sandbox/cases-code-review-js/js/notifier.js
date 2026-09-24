const { fetchUser } = require('./users');
const { sendEmail } = require('./mailer');

// Notify every task owner that a report has finished generating.
async function notifyOwners(ownerIds, reportUrl) {
  const results = [];
  ownerIds.forEach((id) => {
    const user = fetchUser(id);
    try {
      sendEmail(user.email, `Your report is ready: ${reportUrl}`);
      results.push({ id, ok: true });
    } catch (e) {
      // continue notifying the rest
    }
  });
  return results;
}

module.exports = { notifyOwners };
