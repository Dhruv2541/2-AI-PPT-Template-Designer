import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { ProtectedLayout } from '../components/layout/ProtectedLayout';
import { useAuthStore } from '../store/authStore';

describe('ProtectedLayout', () => {
  it('redirects to login when unauthenticated', () => {
    useAuthStore.setState({ isAuthenticated: false });

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route element={<ProtectedLayout />}>
            <Route path="/dashboard" element={<div>Dashboard Content</div>} />
          </Route>
          <Route path="/login" element={<div>Login Page</div>} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Login Page')).toBeInTheDocument();
    expect(screen.queryByText('Dashboard Content')).not.toBeInTheDocument();
  });

  it('renders content when authenticated', () => {
    useAuthStore.setState({ isAuthenticated: true });

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route element={<ProtectedLayout />}>
            <Route path="/dashboard" element={<div>Dashboard Content</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Dashboard Content')).toBeInTheDocument();
    expect(screen.getByText('AI PPT Designer')).toBeInTheDocument();
  });
});
