import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";

export default function UserLeadsPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadLeads = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("token");
      //console.log("TOKEN FROM LS:", token);
      const res = await fetch("/api/user_leads/?limit=50", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      const data = await res.json();
      setItems(data);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadLeads();
  }, [loadLeads]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "crimson" }}>{error}</div>;

  return (
    <div style={{ padding: 20 }}>
      <h1>User Leads</h1>

      <table width="100%" cellPadding="8">
        <thead>
          <tr>
            <th align="left">Title</th>
            <th align="left">Source</th>
            <th align="left">Score</th>
            <th align="left">Created</th>
          </tr>
        </thead>
        <tbody>
          {items.map((ul) => (
            <tr key={ul.id}>
              <td>
                <Link to={`/user_leads/${ul.id}`}>
                  {ul.raw_item?.title ?? "—"}
                </Link>
              </td>
              <td>{ul.raw_item?.source_id ?? "—"}</td>
              <td>{ul.heuristic_score}</td>
              <td>{new Date(ul.created_at).toLocaleString()}</td>
            </tr>
          ))}

          {items.length === 0 && (
            <tr>
              <td colSpan="4" style={{ color: "#666" }}>
                No leads yet
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
