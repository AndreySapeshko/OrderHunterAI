import { useState, useEffect } from "react";

const SOURCES = ["telegram", "kwork_projects", "reddit_forhire"];

function splitLines(text) {
  return text
    .split("\n")
    .map((s) => s.trim())
    .filter(Boolean);
}

function lines(arr) {
  return (arr || []).join("\n");
}

export default function RuleForm({ rule, onSaved, onCancel }) {
  const token = localStorage.getItem("token");

  const [sources, setSources] = useState([]);
  const [include, setInclude] = useState("");
  const [exclude, setExclude] = useState("");
  const [notify, setNotify] = useState("");

  const [minText, setMinText] = useState(200);
  const [minScore, setMinScore] = useState(1);
  const [notifyScore, setNotifyScore] = useState(3);
  const [enabled, setEnabled] = useState(true);

  const isEdit = Boolean(rule);

  useEffect(() => {
    if (!rule) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSources([]);
      setInclude("");
      setExclude("");
      setNotify("");
      setMinText(200);
      setMinScore(1);
      setNotifyScore(3);
      setEnabled(true);
      return;
    }

    // режим редактирования
    setSources(rule.source_ids ?? [])
    setInclude(lines(rule.include_keywords));
    setExclude(lines(rule.exclude_keywords));
    setNotify(lines(rule.keywords_for_notis));
    setMinText(rule.min_text_length ?? 0)
    setMinScore(rule.min_score ?? 0);
    setNotifyScore(rule.min_score_for_notis ?? 0)
    setEnabled(rule.enabled ?? true);
  }, [rule]);

  async function submit() {
    const payload = {
      source_ids: sources.length ? sources : null,
      include_keywords: splitLines(include),
      exclude_keywords: splitLines(exclude),
      keywords_for_notis: splitLines(notify),
      min_text_length: minText,
      min_score: minScore,
      min_score_for_notis: notifyScore,
      enabled,
    };

    const url = isEdit
      ? `/api/user_rules/${rule.id}`
      : "/api/user_rules/";

    const method = isEdit ? "PATCH" : "POST";

    const res = await fetch(url, {
      method: method,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.text();
      alert(err);
      return;
    }

    onSaved();
  }

  if (!rule && isEdit) return null;

  function toggleSource(src) {
    setSources((prev) =>
      prev.includes(src)
        ? prev.filter((s) => s !== src)
        : [...prev, src]
    );
  }

  return (
    <div style={{ border: "1px solid #ddd", padding: 16, marginBottom: 20 }}>
      <h3>{isEdit ? "Edit rule" : "Create rule"}</h3>

      <b>Sources</b>
      <div style={{ marginBottom: 12 }}>
        {SOURCES.map((s) => (
          <label key={s} style={{ marginRight: 12 }}>
            <input
              type="checkbox"
              checked={sources.includes(s)}
              onChange={() => toggleSource(s)}
            />{" "}
            {s}
          </label>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <textarea
          rows={6}
          placeholder="Include keywords (one per line)"
          value={include}
          onChange={(e) => setInclude(e.target.value)}
        />
        <textarea
          rows={6}
          placeholder="Exclude keywords (one per line)"
          value={exclude}
          onChange={(e) => setExclude(e.target.value)}
        />
      </div>

      <textarea
        rows={3}
        placeholder="Notify keywords (optional)"
        value={notify}
        onChange={(e) => setNotify(e.target.value)}
        style={{ width: "100%", marginTop: 12 }}
      />

      <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
        <input
          type="number"
          value={minText}
          onChange={(e) => setMinText(+e.target.value)}
          placeholder="Min text length"
        />
        <input
          type="number"
          value={minScore}
          onChange={(e) => setMinScore(+e.target.value)}
          placeholder="Min score"
        />
        <input
          type="number"
          value={notifyScore}
          onChange={(e) => setNotifyScore(+e.target.value)}
          placeholder="Notify score"
        />
      </div>

      <label style={{ display: "block", marginTop: 12 }}>
        <input
          type="checkbox"
          checked={enabled}
          onChange={() => setEnabled(!enabled)}
        />{" "}
        Enabled
      </label>

      <button onClick={submit} style={{ marginTop: 12 }}>
        Save rule
      </button>
      {isEdit && <button onClick={onCancel}>Cancel</button>}
    </div>
  );
}
