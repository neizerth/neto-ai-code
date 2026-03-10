import { loginUser } from "@/api/auth";
import type { LoginCredentials } from "@/api/auth";
import { useMutation } from "@tanstack/react-query";

export function useLogin() {
  return useMutation({
    mutationFn: (credentials: LoginCredentials) => loginUser(credentials),
  });
}
