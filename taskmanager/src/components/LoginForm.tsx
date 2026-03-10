import { useAuth } from "@/contexts/AuthContext";
import { useLogin } from "@/hooks/useLogin";
import { type LoginFormData, loginSchema } from "@/schemas/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useId } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

export function LoginForm() {
  const emailId = useId();
  const passwordId = useId();
  const navigate = useNavigate();
  const { login } = useAuth();
  const { mutate: doLogin, isPending, isSuccess, error } = useLogin();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  const onSubmit = (data: LoginFormData) => {
    doLogin(data, {
      onSuccess: (res) => {
        login(res.token, { id: res.user.id, email: res.user.email, name: res.user.name });
        navigate("/tasks", { replace: true });
      },
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 max-w-sm">
      <div>
        <label htmlFor={emailId} className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id={emailId}
          type="email"
          {...register("email")}
          className="w-full rounded border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          placeholder="user@example.com"
        />
        {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
      </div>
      <div>
        <label htmlFor={passwordId} className="block text-sm font-medium text-gray-700 mb-1">
          Пароль
        </label>
        <input
          id={passwordId}
          type="password"
          {...register("password")}
          className="w-full rounded border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        />
        {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>}
      </div>
      {error && <p className="text-sm text-red-600">{error.message}</p>}
      {isSuccess && <p className="text-sm text-green-600">Вход выполнен успешно.</p>}
      <button
        type="submit"
        disabled={isPending}
        className="rounded bg-blue-600 px-4 py-2 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {isPending ? "Вход…" : "Войти"}
      </button>
    </form>
  );
}
