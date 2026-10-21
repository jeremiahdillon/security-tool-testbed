// Helpers for ordering and batching outbound reminder jobs.
// Each job looks like { id, priority, dueAt }, where dueAt is a Unix timestamp in seconds.

// Highest priority first; ties go to the job that is due soonest.
function orderJobs(jobs) {
  return jobs.slice().sort((a, b) => b.priority - a.priority || a.dueAt - b.dueAt);
}

// Split jobs into consecutive batches of at most `size`.
function toBatches(jobs, size) {
  const batches = [];
  for (let i = 0; i < jobs.length; i += size) {
    batches.push(jobs.slice(i, i + size));
  }
  return batches;
}

// Jobs that are due to run as of `now`.
function dueJobs(jobs, now = Date.now()) {
  return jobs.filter((job) => job.dueAt <= now);
}

module.exports = { orderJobs, toBatches, dueJobs };
