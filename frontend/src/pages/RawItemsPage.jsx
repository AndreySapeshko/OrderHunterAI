import { useEffect, useState } from "react";

export default function RawItemsPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetch("/api/raw_items?limit=50", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((r) => r.json())
      .then(setItems)
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <>
      <h1>Raw items</h1>

      {loading && <div>Loading...</div>}

      <table width="100%" cellPadding="8">
        <thead>
          <tr>
            <th align="left">Title</th>
            <th align="left">Source</th>
            <th align="left">Price</th>
            <th align="left">Score</th>
          </tr>
        </thead>
        <tbody>
          {items.map((it) => (
            <tr key={it.id}>
              <td>{it.title}</td>
              <td>{it.source_id}</td>
              <td>
                {it.price_limit || "-"} / {it.possible_price_limit || "-"}
              </td>
              <td>{it.heuristic_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
