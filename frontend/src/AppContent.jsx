import { Routes, Route, Link } from "react-router-dom";
import RawItemsPage from "./pages/RawItemsPage.jsx";
import UserLeadsPage from "./pages/UserLeadsPage";
import UserLeadDetailPage from "./pages/UserLeadDetailPage.jsx";
import RequireAuth, { RequireAdmin } from "./auth/RequireAuth";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AdminUsersPage from "./pages/AdminUsersPage";
import { useAuth } from "./auth/useAuth";

export default function AppContent() {
  const { user, logout } = useAuth();

  return (
    <div style={{ padding: 20, fontFamily: "system-ui" }}>
      <nav style={{ marginBottom: 20 }}>
        <Link to="/raw_items">Raw items</Link>
        {" | "}
        <Link to="/user_leads">My leads</Link>

        {user?.is_admin && (
          <>
            {" | "}
            <Link to="/admin/users">Admin</Link>
          </>
        )}

        {user ? (
          <>
            {" | "}
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            {" | "}
            <Link to="/login">Login</Link>
            {" | "}
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>

      <Routes>
        {/* public */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* protected */}
        <Route
          path="/"
          element={
            <RequireAuth>
              <UserLeadsPage />
            </RequireAuth>
          }
        />

        <Route
          path="/user_leads"
          element={
            <RequireAuth>
              <UserLeadsPage />
            </RequireAuth>
          }
        />

        <Route
          path="/user_leads/:id"
          element={
            <RequireAuth>
              <UserLeadDetailPage />
            </RequireAuth>
          }
        />

        <Route
          path="/raw_items"
          element={
            <RequireAuth>
              <RawItemsPage />
            </RequireAuth>
          }
        />

        <Route
          path="/admin/users"
          element={
            <RequireAuth>
              <RequireAdmin>
                <AdminUsersPage />
              </RequireAdmin>
            </RequireAuth>
          }
        />

        <Route path="*" element={<div>Not found</div>} />
      </Routes>
    </div>
  );
}
