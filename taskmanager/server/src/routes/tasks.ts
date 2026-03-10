import { Router } from "express";
import type { AuthRequest } from "../middleware/auth.js";
import { authMiddleware } from "../middleware/auth.js";
import {
  createTask,
  deleteTask,
  getTaskById,
  getTasksByUserId,
  updateTask,
} from "../store/tasks.js";

export const tasksRouter = Router();

tasksRouter.use(authMiddleware);

function getUserId(req: AuthRequest): number {
  const id = req.userId;
  if (id === undefined) throw new Error("Auth middleware must set userId");
  return id;
}

tasksRouter.get("/", (req, res) => {
  const userId = getUserId(req as AuthRequest);
  const tasks = getTasksByUserId(userId);
  res.json(tasks);
});

tasksRouter.get("/:id", (req, res) => {
  const userId = getUserId(req as AuthRequest);
  const id = Number(req.params.id);
  if (!Number.isInteger(id)) {
    return res.status(400).json({ message: "Некорректный id" });
  }
  const task = getTaskById(id, userId);
  if (!task) return res.status(404).json({ message: "Задача не найдена" });
  res.json(task);
});

tasksRouter.post("/", (req, res) => {
  const userId = getUserId(req as AuthRequest);
  const { title, dueDate } = req.body ?? {};
  if (!title || typeof title !== "string" || !title.trim()) {
    return res.status(400).json({ message: "Нужно поле title" });
  }
  const task = createTask(userId, title, dueDate);
  res.status(201).json(task);
});

tasksRouter.patch("/:id", (req, res) => {
  const userId = getUserId(req as AuthRequest);
  const id = Number(req.params.id);
  if (!Number.isInteger(id)) {
    return res.status(400).json({ message: "Некорректный id" });
  }
  const { title, completed, dueDate } = req.body ?? {};
  const patch: { title?: string; completed?: boolean; dueDate?: string | null } = {};
  if (typeof title === "string") patch.title = title;
  if (typeof completed === "boolean") patch.completed = completed;
  if (dueDate !== undefined) patch.dueDate = dueDate;
  if (Object.keys(patch).length === 0) {
    return res.status(400).json({ message: "Нужно передать title или completed" });
  }
  const task = updateTask(id, userId, patch);
  if (!task) return res.status(404).json({ message: "Задача не найдена" });
  res.json(task);
});

tasksRouter.delete("/:id", (req, res) => {
  const userId = getUserId(req as AuthRequest);
  const id = Number(req.params.id);
  if (!Number.isInteger(id)) {
    return res.status(400).json({ message: "Некорректный id" });
  }
  const deleted = deleteTask(id, userId);
  if (!deleted) return res.status(404).json({ message: "Задача не найдена" });
  res.status(204).send();
});
