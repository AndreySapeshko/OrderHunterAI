import { useEffect, useState } from "react";

export default function App() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadLeads() {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/leads?limit=50");
      if (!res.ok) throw new Error(`Failed to load leads: ${res.status}`);
      const data = await res.json();
      setLeads(data);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

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
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "system-ui" }}>
      <h1 style={{ marginTop: 0 }}>AI Leads</h1>

      <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 12 }}>
        <button onClick={loadLeads} disabled={loading}>
          {loading ? "Loading..." : "Refresh"}
        </button>
        {error ? <span style={{ color: "crimson" }}>{error}</span> : null}
      </div>

      <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>Title</th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>Status</th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>Score</th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>Category</th>
            <th align="left" style={{ borderBottom: "1px solid #ccc" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id}>
              <td style={{ borderBottom: "1px solid #eee" }}>{lead.title}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{lead.status}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{lead.ai?.score ?? "-"}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{lead.ai?.category ?? "-"}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                <button onClick={() => updateStatus(lead.id, "saved")}>Save</button>{" "}
                <button onClick={() => updateStatus(lead.id, "rejected")}>Reject</button>{" "}
                <button onClick={() => updateStatus(lead.id, "in_progress")}>In Progress</button>
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
