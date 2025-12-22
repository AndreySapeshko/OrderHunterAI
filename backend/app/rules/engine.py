from backend.app.db.models.user_rule import UserRule


class RuleEngine:
    def __init__(self, rules: list[UserRule]):
        self.rules = [r for r in rules if r.enabled]

    def match(self, lead, lead_ai) -> bool:
        for rule in self.rules:
            if not self._match_rule(rule, lead, lead_ai):
                return False
        return True

    def _match_rule(self, rule, lead, lead_ai) -> bool:
        if lead_ai.score < rule.min_score:
            return False

        if rule.categories and lead_ai.category not in rule.categories:
            return False

        text = (lead.title + " " + lead.description).lower()

        if rule.include_keywords:
            if not any(k.lower() in text for k in rule.include_keywords):
                return False

        if rule.exclude_keywords:
            if any(k.lower() in text for k in rule.exclude_keywords):
                return False

        return True
