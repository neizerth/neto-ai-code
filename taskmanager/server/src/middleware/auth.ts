import type { NextFunction, Request, Response } from "express";

export interface AuthRequest extends Request {
  userId?: number;
}

export function authMiddleware(req: AuthRequest, res: Response, next: NextFunction): void {
  const header = req.headers.authorization;
  const token = header?.startsWith("Bearer ") ? header.slice(7) : null;
  if (!token) {
    res.status(401).json({ message: "Требуется авторизация" });
    return;
  }
  const match = /^jwt-(\d+)-/.exec(token);
  const userId = match ? Number(match[1]) : Number.NaN;
  if (!Number.isInteger(userId) || userId < 1) {
    res.status(401).json({ message: "Неверный токен" });
    return;
  }
  req.userId = userId;
  next();
}
