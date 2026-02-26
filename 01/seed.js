const { faker } = require('@faker-js/faker');
const db = require('./db');

// Функция для заполнения тестовыми данными
function seedUsers(count = 10) {
  const insert = db.prepare('INSERT INTO users (email, name) VALUES (?, ?)');

  for (let i = 0; i < count; i++) {
    const email = faker.internet.email();
    const name = faker.person.fullName();
    insert.run(email, name);
  }

  insert.finalize();
  console.log(`${count} пользователей добавлено в базу данных.`);
}

seedUsers();

// Закрываем соединение с базой данных
db.close((err) => {
  if (err) {
    console.error('Ошибка при закрытии базы данных:', err.message);
  } else {
    console.log('Соединение с базой данных закрыто.');
  }
});