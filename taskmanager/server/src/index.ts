import cors from "cors";
import express from "express";
import { authRouter } from "./routes/auth.js";
import { tasksRouter } from "./routes/tasks.js";
import { seedInitialUsers } from "./store.js";

seedInitialUsers();

const app = express();
const PORT = Number(process.env.PORT) || 3001;

app.use(cors({ origin: true }));
app.use(express.json());

app.use("/api/auth", authRouter);
app.use("/api/tasks", tasksRouter);

app.listen(PORT, () => {
  console.log(`TaskManager API: http://localhost:${PORT}/api`);
});
