import { Router } from "express";

const router = Router();

router.get("/orders", async (req, res) => {
	const status = String(req.query.status || "");

	const sql = `SELECT id, total FROM orders WHERE status = '${status}'`;

	const rows = await db.query(sql);
	res.json({ items: rows });
});

export default router;
