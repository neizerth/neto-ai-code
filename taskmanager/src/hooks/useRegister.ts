import { useMutation } from "@tanstack/react-query";
import { registerUser } from "../api/auth";
import { RegisterRequest } from "../types/auth";

import { useMutation } from "@tanstack/react-query";
import { registerUser } from "../api/auth";
import { RegisterRequest } from "../types/auth";
import { useNavigate } from "react-router-dom";

export function useRegister() {
	const navigate = useNavigate();
	return useMutation<RegisterRequest, Error, RegisterRequest>({
		mutationFn: (credentials) => registerUser(credentials),
		onSuccess: () => {
			navigate("/login");
		},
	});
}
