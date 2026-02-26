const db = require('../database/db');

async function getUsers() {
  return new Promise((resolve, reject) => {
    const query = 'SELECT * FROM users';
    db.all(query, [], (err, rows) => {
      if (err) {
        reject(err);
      } else {
        resolve(rows);
      }
    });
  });
}

module.exports = getUsers;