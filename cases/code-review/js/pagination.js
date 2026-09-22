// Utility helpers for paginating result sets in the reporting dashboard.

// Return the slice of `items` for the given 1-indexed page.
function paginate(items, page, pageSize) {
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  return items.slice(start, end);
}

// Return the last full window of `items` (the most recent `pageSize` entries).
function lastWindow(items, pageSize) {
  const result = [];
  for (let i = items.length - pageSize; i <= items.length; i++) {
    result.push(items[i]);
  }
  return result;
}

module.exports = { paginate, lastWindow };
