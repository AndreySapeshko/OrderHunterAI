import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

export default function UserLeadDetailPage() {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetch(`/api/user_leads/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((r) => r.json())
      .then(setLead);
  }, [id, token]);

  if (!lead) return <div>Loading...</div>;

  const raw = lead.raw_item;
  const ai = lead.lead.ai;

  return (
    <>
      <Link to="/user_leads">← Back</Link>

      <h2>{raw?.title}</h2>

      <p>
        <b>Source:</b> {raw?.source_id}<br />
        <b>Price:</b> {raw?.price_limit} – {raw?.possible_price_limit}<br />
        <b>Score:</b> {raw?.heuristic_score}
      </p>

      <h3>Description</h3>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {raw?.content}
      </pre>

      {ai && (
        <>
          <h3>AI Analysis</h3>
          <pre>{JSON.stringify(ai, null, 2)}</pre>
        </>
      )}

      <a href={raw?.url} target="_blank" rel="noreferrer">
        Open original
      </a>
    </>
  );
}
