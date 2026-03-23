import { useId } from "react";
import { useRegistrationForm } from "../hooks/useRegistrationForm";
import { RegistrationFormData } from "../schemas/registrationSchema";
import { FormField } from "./FormField";

interface RegistrationFormProps {
	onSuccess: () => void;
}

export function RegistrationForm({ onSuccess }: RegistrationFormProps) {
	const emailId = useId();
	const passwordId = useId();
	const { register, handleSubmit, errors, isPending, error, onSubmit } =
		useRegistrationForm(onSuccess);

	return (
		<form
			onSubmit={handleSubmit(onSubmit)}
			className="flex flex-col gap-4 max-w-sm"
		>
			<FormField
				id={emailId}
				label="Email"
				type="email"
				error={errors.email?.message}
				disabled={isPending}
				register={register}
			/>
			<FormField
				id={passwordId}
				label="Пароль"
				type="password"
				error={errors.password?.message}
				disabled={isPending}
				register={register}
			/>
			{error && (
				<p className="text-sm text-red-600">
					{error.status === 409
						? "Пользователь с таким email уже существует."
						: `Ошибка: ${error.message}`}
				</p>
			)}
			<button
				type="submit"
				disabled={isPending}
				className="rounded bg-blue-600 px-4 py-2 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
			>
				{isPending ? "Загрузка..." : "Зарегистрироваться"}
			</button>
		</form>
	);
}
