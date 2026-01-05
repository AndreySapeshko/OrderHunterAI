import { useEffect, useState } from "react";
import RuleItem from "../components/RuleItem";
import RuleForm from "../components/RuleForm";

export default function RulesPage() {
  const [rules, setRules] = useState([]);
  const [editingRule, setEditingRule] = useState(null);
  const token = localStorage.getItem("token");

  const loadRules = async () => {
    const res = await fetch("/api/user_rules/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setRules(await res.json());
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadRules();
  }, []);

  return (
    <>
      <RuleForm
        rule={editingRule}
        onSaved={() => {
          setEditingRule(null);
          loadRules();
        }}
        onCancel={() => setEditingRule(null)}
      />

      {rules.map((rule) => (
        <RuleItem
          key={rule.id}
          rule={rule}
          onEdit={() => setEditingRule(rule)}
          onChange={loadRules}
        />
      ))}
    </>
  );
}

