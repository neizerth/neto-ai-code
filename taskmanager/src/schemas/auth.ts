import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().min(1, "Введите email").email("Некорректный email"),
  password: z.string().min(1, "Введите пароль"),
});

export type LoginFormData = z.infer<typeof loginSchema>;

// TODO: Добавить registrationSchema (Zod) для формы регистрации:
// - email (обязательный, формат email)
// - password (обязательный, минимум 6 символов)
// Экспортировать тип RegistrationFormData (API принимает только email и password)
