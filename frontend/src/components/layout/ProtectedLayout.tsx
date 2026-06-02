import { Navigate, Outlet, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const ProtectedLayout = () => {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-6">
          <h1 className="text-xl font-bold text-indigo-600">AI PPT Designer</h1>
          <nav className="flex space-x-4">
            <Link to="/dashboard" className="text-gray-600 hover:text-gray-900 font-medium">Dashboard</Link>
            <Link to="/templates" className="text-gray-600 hover:text-gray-900 font-medium">Templates</Link>
          </nav>
        </div>
        <button
          onClick={() => useAuthStore.getState().logout()}
          className="text-sm text-gray-600 hover:text-gray-900 font-medium"
        >
          Logout
        </button>
      </header>
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
        <Outlet />
      </main>
    </div>
  );
};
