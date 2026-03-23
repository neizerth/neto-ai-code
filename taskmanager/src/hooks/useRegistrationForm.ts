import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { registrationSchema, type RegistrationFormData } from "../schemas/registrationSchema";
import { useRegister } from "../hooks/useRegister";

export function useRegistrationForm(onSuccess: () => void) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
  });

  const { mutate, isPending, error } = useRegister();

  const onSubmit = (data: RegistrationFormData) => {
    mutate(data, {
      onSuccess: () => {
        onSuccess();
        reset();
      },
    });
  };

  return {
    register,
    handleSubmit,
    errors,
    isPending,
    error,
    onSubmit,
  };
}
