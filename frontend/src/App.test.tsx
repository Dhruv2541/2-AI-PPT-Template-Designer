import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders without crashing and shows login or dashboard', () => {
    render(<App />);
    // App router redirects to /dashboard, which redirects to /login if unauthenticated
    expect(screen.getByText(/Sign in to your account/i)).toBeInTheDocument();
  });
});
