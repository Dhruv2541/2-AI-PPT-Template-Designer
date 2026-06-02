import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const ProtectedLayout = () => {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">AI PPT Designer</h1>
        <button
          onClick={() => useAuthStore.getState().logout()}
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          Logout
        </button>
      </header>
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
};
