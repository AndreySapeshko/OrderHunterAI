import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

export default function UserLeadDetailPage() {
  const { id } = useParams();
  const [lead, setLead] = useState(null);

  useEffect(() => {
    fetch(`/api/user-leads/${id}`)
      .then((r) => r.json())
      .then(setLead);
  }, [id]);

  if (!lead) return <div>Loading...</div>;

  return (
    <>
      <Link to="/leads">← Back</Link>

      <h2>{lead.title}</h2>

      <p>
        <b>Source:</b> {lead.source_id}<br />
        <b>Price:</b> {lead.price_limit} – {lead.possible_price_limit}<br />
        <b>Score:</b> {lead.heuristic_score}
      </p>

      <h3>Description</h3>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {lead.content}
      </pre>

      {lead.ai && (
        <>
          <h3>AI Analysis</h3>
          <pre>{JSON.stringify(lead.ai, null, 2)}</pre>
        </>
      )}

      <a href={lead.url} target="_blank" rel="noreferrer">
        Open original
      </a>
    </>
  );
}
