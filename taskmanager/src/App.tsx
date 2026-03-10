import { LoginForm } from "@/components/LoginForm";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { RegistrationForm } from "@/components/RegistrationForm";
import { useAuth } from "@/contexts/AuthContext";
import { TasksPage } from "@/pages/TasksPage";
import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router-dom";

function Layout({ children }: { children: React.ReactNode }) {
  const { token, user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-xl font-semibold text-gray-800">
            TaskManager
          </Link>
          <nav className="flex gap-4">
            {token ? (
              <>
                <Link to="/tasks" className="text-blue-600 hover:underline">
                  Мои задачи
                </Link>
                <span className="text-gray-500 text-sm">{user?.email}</span>
                <button type="button" onClick={logout} className="text-blue-600 hover:underline">
                  Выйти
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-blue-600 hover:underline">
                  Вход
                </Link>
                <Link to="/register" className="text-blue-600 hover:underline">
                  Регистрация
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="flex-1 flex items-center justify-center p-4">{children}</main>
    </div>
  );
}

function HomePage() {
  const { token, isReady } = useAuth();
  if (!isReady) return <p className="text-gray-500">Загрузка…</p>;
  if (token) return <Navigate to="/tasks" replace />;
  return (
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Добро пожаловать в TaskManager</h1>
      <p className="text-gray-600 mb-4">Войдите или зарегистрируйтесь, чтобы начать.</p>
      <div className="flex gap-4 justify-center">
        <Link
          to="/login"
          className="rounded bg-blue-600 px-4 py-2 text-white font-medium hover:bg-blue-700"
        >
          Войти
        </Link>
        <Link
          to="/register"
          className="rounded border border-gray-300 bg-white px-4 py-2 text-gray-700 font-medium hover:bg-gray-50"
        >
          Регистрация
        </Link>
      </div>
    </div>
  );
}

function LoginPage() {
  const { token, isReady } = useAuth();
  if (isReady && token) return <Navigate to="/tasks" replace />;
  return (
    <div className="w-full max-w-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Вход</h2>
      <LoginForm />
    </div>
  );
}

function RegisterPage() {
  return (
    <div className="w-full max-w-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Регистрация</h2>
      <RegistrationForm />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/tasks"
            element={
              <ProtectedRoute>
                <TasksPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
