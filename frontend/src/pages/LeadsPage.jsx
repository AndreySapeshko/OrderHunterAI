import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";

export default function App() {
  const [statusFilter, setStatusFilter] = useState("");
  const [minScore, setMinScore] = useState("");

  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadLeads = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const params = new URLSearchParams();

      if (statusFilter) params.append("status", statusFilter);
      if (minScore) params.append("min_score", minScore);

      params.append("limit", "50");

      const res = await fetch(`/api/leads?${params.toString()}`);
      if (!res.ok) throw new Error(`Failed to load leads: ${res.status}`);
      const data = await res.json();
      setLeads(data);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, [statusFilter, minScore]);

  async function updateStatus(id, status) {
    setError("");
    try {
      const res = await fetch(`/api/leads/${id}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) {
        const body = await res.text();
        throw new Error(`Failed to update status: ${res.status} ${body}`);
      }
      await loadLeads();
    } catch (e) {
      setError(String(e));
    }
  }

  useEffect(() => {
    loadLeads();
  }, [loadLeads]);

  return (
    <div style={{ padding: 20, fontFamily: "system-ui" }}>
      <h1 style={{ marginTop: 0 }}>AI Leads</h1>

      <div
        style={{
          display: "flex",
          gap: 12,
          alignItems: "center",
          marginBottom: 12,
        }}
      >
        <button onClick={loadLeads} disabled={loading}>
          {loading ? "Loading..." : "Refresh"}
        </button>
        {error ? <span style={{ color: "crimson" }}>{error}</span> : null}
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All statuses</option>
          <option value="new">New</option>
          <option value="saved">Saved</option>
          <option value="rejected">Rejected</option>
          <option value="in_progress">In Progress</option>
        </select>

        <input
          type="number"
          placeholder="Min score"
          value={minScore}
          onChange={(e) => setMinScore(e.target.value)}
          style={{ width: 100 }}
        />

        <button onClick={loadLeads}>Apply</button>
      </div>

      <table
        width="100%"
        cellPadding="8"
        style={{ borderCollapse: "collapse" }}
      >
        <thead>
          <tr>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>
              Title
            </th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>
              Status
            </th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>
              Score
            </th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>
              Category
            </th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id}>
              <td style={{ borderBottom: "1px solid #eee" }}>
                <Link to={`/lead/${lead.id}`}>{lead.title}</Link>
              </td>
              <td style={{ borderBottom: "1px solid #eee" }}>{lead.status}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                {lead.ai?.score ?? "-"}
              </td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                {lead.ai?.category ?? "-"}
              </td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                <button onClick={() => updateStatus(lead.id, "saved")}>
                  Save
                </button>{" "}
                <button onClick={() => updateStatus(lead.id, "rejected")}>
                  Reject
                </button>{" "}
                <button onClick={() => updateStatus(lead.id, "in_progress")}>
                  In Progress
                </button>
              </td>
            </tr>
          ))}
          {leads.length === 0 && !loading ? (
            <tr>
              <td colSpan="5" style={{ padding: 12, color: "#666" }}>
                No leads yet. Start ingestion and click Refresh.
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}
