import { apiRequest } from "./client";

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: { id: string; email: string; name: string };
}

export async function loginUser(credentials: LoginCredentials): Promise<LoginResponse> {
  return apiRequest<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

// TODO: Реализовать registerUser для POST /api/auth/register
// Request: { email: string, password: string }
// Response 201: { id: number, email: string, createdAt: string }
// При 409 (email занят) — показать ошибку в форме
