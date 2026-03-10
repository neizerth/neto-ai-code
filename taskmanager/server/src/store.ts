export interface User {
  id: number;
  email: string;
  password: string;
  createdAt: string;
}

const users = new Map<string, User>();
let nextId = 1;

/** Предзаполнение тестовыми пользователями при старте сервера */
export function seedInitialUsers(): void {
  if (users.size > 0) return;
  const initial: User[] = [
    {
      id: 1,
      email: "demo@taskmanager.local",
      password: "demo",
      createdAt: "2025-01-01T00:00:00.000Z",
    },
    {
      id: 2,
      email: "test@example.com",
      password: "test123",
      createdAt: "2025-01-01T00:00:00.000Z",
    },
    {
      id: 3,
      email: "admin@taskmanager.local",
      password: "admin",
      createdAt: "2025-01-01T00:00:00.000Z",
    },
  ];
  for (const u of initial) {
    users.set(u.email, u);
  }
  nextId = initial.length + 1;
}

export function findByEmail(email: string): User | undefined {
  return users.get(email.toLowerCase());
}

export function createUser(email: string, password: string): User {
  const normalized = email.toLowerCase();
  if (users.has(normalized)) {
    const err = new Error("Email уже занят") as Error & { statusCode?: number };
    err.statusCode = 409;
    throw err;
  }
  const user: User = {
    id: nextId++,
    email: normalized,
    password,
    createdAt: new Date().toISOString(),
  };
  users.set(normalized, user);
  return user;
}

export function checkPassword(user: User, password: string): boolean {
  return user.password === password;
}
