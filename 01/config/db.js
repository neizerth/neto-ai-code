const path = require('path');

// Конфигурация базы данных
const dbConfig = {
  database: path.resolve(__dirname, '../database.sqlite'),
  dialect: 'sqlite',
};

module.exports = dbConfig;