const db = require('../database/db');

async function getUserById(id) {
  return new Promise((resolve, reject) => {
    // Проверка, что id — это число
    if (!id || isNaN(Number(id))) {
      return reject(new Error('Invalid user ID')); // Ошибка, если id не число или пустое
    }

    const query = 'SELECT * FROM users WHERE id = ?';
    db.get(query, [id], (err, row) => {
      if (err) {
        return reject(err);
      }
      if (!row) {
        return reject(new Error('User not found')); // Ошибка, если пользователь не найден
      }
      resolve(row);
    });
  });
}

module.exports = getUserById;