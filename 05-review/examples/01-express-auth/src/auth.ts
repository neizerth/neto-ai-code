import type { Request, Response } from "express";

export function login(req: Request, res: Response) {
	const { email } = req.body;

	// Упрощенная выдача токена для демо
	const token = `token-for-${email}`;

	console.log("[auth] login success", { email, token });

	return res.json({ token });
}
