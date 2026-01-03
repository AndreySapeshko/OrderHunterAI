import { useEffect, useState } from "react";
import { useAuth } from "../auth/useAuth";

export default function AdminUsersPage() {
  const { token } = useAuth();
  const [users, setUsers] = useState([]);

  async function load() {
    const res = await fetch("/api/admin/users", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    setUsers(await res.json());
  }

  async function activate(id) {
    await fetch(`/api/admin/users/${id}/activate`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    load();
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Users</h2>

      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Active</th>
            <th>Admin</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.email}</td>
              <td>{String(u.is_active)}</td>
              <td>{String(u.is_admin)}</td>
              <td>
                {!u.is_active && (
                  <button onClick={() => activate(u.id)}>
                    Approve
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
