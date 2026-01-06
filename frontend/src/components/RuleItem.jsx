export default function RuleItem({ rule,onEdit, onChange }) {
  const token = localStorage.getItem("token");

  const toggle = async () => {
    await fetch(`/api/user_rules/${rule.id}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ enabled: !rule.enabled }),
    });
    onChange();
  };

  const remove = async () => {
    await fetch(`/api/user_rules/${rule.id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    onChange();
  };

  return (
    <div style={{ borderBottom: "1px solid #ddd", padding: 8 }}>
      <label>
        <input type="checkbox" checked={rule.enabled} onChange={toggle} />{" "}
        <b>{rule.source_id || "any source"}</b>
      </label>

      <div>
        include: {(rule.include_keywords || []).join(", ")}
      </div>
      <div>
        exclude: {(rule.exclude_keywords || []).join(", ")}
      </div>
      <div>
        min score: {rule.min_score}
      </div>

      <button onClick={onEdit}>✏️ Edit</button>

      <button onClick={remove} style={{ color: "crimson" }}>
        Delete
      </button>
    </div>
  );
}
