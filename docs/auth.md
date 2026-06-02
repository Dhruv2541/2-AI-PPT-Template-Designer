# Authentication Architecture

The AI PPT Designer uses JWT-based authentication.

## Phase 2: Mock Authentication (Current)

To accelerate frontend and core feature development, a Mock Authentication flow is currently implemented.

### Flow
1. User clicks "Mock Login" on the `/login` page.
2. Frontend sends a `POST` request to `/api/auth/mock-login` with dummy user data.
3. Backend creates or fetches the dummy user from the `users` table.
4. Backend issues a real JWT signed with `JWT_SECRET_KEY` and returns it.
5. Frontend stores the JWT in `localStorage` and Zustand state, and redirects to `/dashboard`.
6. Subsequent requests (like `/api/auth/me`) include the `Authorization: Bearer <token>` header.

## Phase 10: Google OAuth Integration (Future)

Before production deployment, the Mock Auth will be swapped for Google OAuth.

### Planned Flow
1. User clicks "Sign in with Google" on the `/login` page.
2. Frontend uses `@react-oauth/google` to display the Google consent screen.
3. Google returns a `credential` (Google JWT) to the frontend.
4. Frontend sends `POST /api/auth/google-login` containing the Google JWT.
5. Backend verifies the Google JWT signature using Google's public JWKs.
6. Backend extracts `email`, `name`, `sub` (Google ID), and `picture`.
7. Backend upserts the user in the database.
8. Backend issues our own application JWT and returns it.
9. App proceeds normally.

## Security
- All protected endpoints use `flask-jwt-extended`'s `@jwt_required()` decorator.
- The React frontend uses a `ProtectedLayout` to guard private routes.
