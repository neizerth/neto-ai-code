import { z } from "zod";

export const registrationSchema = z.object({
  email: z.string().min(1, "Введите email").email("Некорректный email"),
  password: z.string().min(8, "Пароль должен быть не менее 8 символов"),
});

export type RegistrationFormData = z.infer<typeof registrationSchema>;
