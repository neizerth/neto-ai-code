/** Ошибка от API с кодом статуса (для обработки 409 и др. в формах) */
export type ApiError = Error & { status?: number };

export function isApiError(e: unknown): e is ApiError {
  return e instanceof Error && "status" in e;
}
