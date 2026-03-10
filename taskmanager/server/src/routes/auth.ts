import { Router } from "express";
import { checkPassword, createUser, findByEmail } from "../store.js";

export const authRouter = Router();

authRouter.post("/register", (req, res) => {
  const { email, password } = req.body ?? {};
  if (!email || typeof email !== "string" || !password || typeof password !== "string") {
    return res.status(400).json({ message: "Нужны email и password" });
  }
  try {
    const user = createUser(email.trim(), password);
    return res.status(201).json({
      id: user.id,
      email: user.email,
      createdAt: user.createdAt,
    });
  } catch (err: unknown) {
    const e = err as Error & { statusCode?: number };
    if (e.statusCode === 409) {
      return res.status(409).json({ message: e.message });
    }
    throw err;
  }
});

authRouter.post("/login", (req, res) => {
  const { email, password } = req.body ?? {};
  if (!email || typeof email !== "string" || !password) {
    return res.status(400).json({ message: "Нужны email и password" });
  }
  const user = findByEmail(email.trim());
  if (!user || !checkPassword(user, password)) {
    return res.status(401).json({ message: "Неверные учётные данные" });
  }
  const token = `jwt-${user.id}-${Date.now()}`;
  return res.json({
    token,
    user: {
      id: String(user.id),
      email: user.email,
      name: user.email.split("@")[0],
    },
  });
});
