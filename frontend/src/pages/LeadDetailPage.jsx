import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

export default function LeadDetailPage() {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`/api/leads/${id}`)
      .then((r) => r.json())
      .then(setLead)
      .catch(() => setError("Failed to load lead"));
  }, [id]);

  if (error) return <div>{error}</div>;
  if (!lead) return <div>Loading...</div>;

  return (
    <div style={{ padding: 20 }}>
      <Link to="/">← Back</Link>

      <h2>{lead.title}</h2>

      <p>
        <b>Status:</b> {lead.status}<br />
        <b>Author:</b> {lead.author}<br />
        <b>Source:</b> {lead.source}<br />
        <b>URL:</b>{" "}
        <a href={lead.url} target="_blank" rel="noreferrer">
          open
        </a>
      </p>

      <h3>Description</h3>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {lead.description}
      </pre>

      {lead.ai && (
        <>
          <h3>AI Analysis</h3>
          <p>
            <b>Relevant:</b> {String(lead.ai.is_relevant)}<br />
            <b>Category:</b> {lead.ai.category}<br />
            <b>Score:</b> {lead.ai.score}
          </p>

          <h4>Extracted</h4>
          <pre>
            {JSON.stringify(lead.ai.extracted, null, 2)}
          </pre>
        </>
      )}
    </div>
  );
}
