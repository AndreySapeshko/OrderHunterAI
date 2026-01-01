import { useState, useCallback } from "react";
import { Link } from "react-router-dom";

export default function UserLeadsPage() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  

  const loadLeads = useCallback(async () => {
    setLoading(true);
    const res = await fetch("/api/user-leads?limit=50");
    const data = await res.json();
    setLeads(data);
    setLoading(false);
  }, []);

  if (loading && leads.length === 0) {
    loadLeads();
  }

  return (
    <>
      <h1>My leads</h1>

      <button onClick={loadLeads} disabled={loading}>
        Refresh
      </button>

      <table width="100%" cellPadding="8">
        <thead>
          <tr>
            <th align="left">Title</th>
            <th align="left">Score</th>
            <th align="left">Source</th>
            <th align="left">Telegram</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((l) => (
            <tr key={l.id}>
              <td>
                <Link to={`/leads/${l.id}`}>{l.title}</Link>
              </td>
              <td>{l.heuristic_score}</td>
              <td>{l.source_id}</td>
              <td>{l.sent_to_telegram ? "✅" : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
