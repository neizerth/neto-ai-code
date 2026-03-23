import React from "react";

interface FormFieldProps {
  id: string;
  label: string;
  type?: string;
  error?: string;
  disabled?: boolean;
  register: any; // React Hook Form register function
}

export function FormField({
  id,
  label,
  type = "text",
  error,
  disabled = false,
  register,
}: FormFieldProps) {
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700">
        {label}
      </label>
      <input
        id={id}
        type={type}
        {...register(id)}
        className="w-full rounded border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        disabled={disabled}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
}
