// TODO: Реализовать форму регистрации по аналогии с LoginForm:
// - useForm + zodResolver(registrationSchema)
// - Поля: email, password (API не принимает name)
// - useRegister() для отправки
// - При ошибке 409 (email занят) — показать сообщение в форме (error.status === 409)

export function RegistrationForm() {
  return (
    <div className="rounded border border-amber-200 bg-amber-50 p-4 max-w-sm">
      <p className="text-amber-800 font-medium">Форма регистрации не реализована</p>
      <p className="text-sm text-amber-700 mt-1">
        Нужно: registerUser (POST /api/auth/register), useRegister, registrationSchema, форма email
        + password. При 409 показывать ошибку в форме.
      </p>
    </div>
  );
}
