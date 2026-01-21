import { Navigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth";

export default function RequireAuth({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;

  return children;
}

export function RequireAdmin({ children }) {
  const { user } = useAuth();

  if (!user?.is_admin) {
    return <div>Access denied</div>;
  }

  return children;
}
