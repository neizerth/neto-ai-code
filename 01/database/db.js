const sqlite3 = require('sqlite3').verbose();
const dbConfig = require('./config');

// Подключаемся к базе данных SQLite
const db = new sqlite3.Database(dbConfig.database);

// Создаём таблицу users
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL
    )
  `);
});

module.exports = db;