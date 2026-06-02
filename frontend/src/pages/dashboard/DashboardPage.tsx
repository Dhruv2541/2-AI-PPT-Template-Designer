import { useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';

export const DashboardPage = () => {
  const { user, token, setAuth } = useAuthStore();

  useEffect(() => {
    // Fetch profile if we have token but no user object
    const fetchProfile = async () => {
      if (token && !user) {
        try {
          const res = await fetch('/api/auth/me', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (res.ok) {
            const data = await res.json();
            setAuth(data, token);
          }
        } catch (err) {
          console.error("Failed to fetch profile", err);
        }
      }
    };
    fetchProfile();
  }, [token, user, setAuth]);

  return (
    <div className="bg-white p-8 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Welcome back{user?.name ? `, ${user.name}` : ''}!</h2>
      <div className="space-y-4">
        <div className="flex items-center space-x-4">
          {user?.avatar_url && (
            <img src={user.avatar_url} alt="Avatar" className="w-16 h-16 rounded-full" />
          )}
          <div>
            <p className="text-gray-600">Email: {user?.email}</p>
            <p className="text-gray-600">ID: {user?.id}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
