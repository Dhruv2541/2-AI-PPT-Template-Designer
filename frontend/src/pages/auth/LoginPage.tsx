import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const LoginPage = () => {
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleMockLogin = async () => {
    try {
      const response = await fetch('/api/auth/mock-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: "mockstudent@example.com",
          name: "Mock Student"
        })
      });

      const data = await response.json();

      if (response.ok && data.access_token) {
        setAuth(data.user, data.access_token);
        navigate('/dashboard');
      }
    } catch (error) {
      console.error("Mock login failed", error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Phase 2: Mock Authentication
          </p>
        </div>
        <button
          onClick={handleMockLogin}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Mock Login as Test Student
        </button>
      </div>
    </div>
  );
};
