import logging

from backend.app.db import RawItem
from backend.app.db.models.user_rule import UserRule

logger = logging.getLogger(__name__)


class RuleEngine:
    def __init__(self, rules: list[UserRule]):
        self.rules = [r for r in rules if r.enabled]

    def match(self, raw: RawItem, sourse_id: str) -> tuple[bool, int]:
        match = True
        score = 0
        for rule in self.rules:
            if not rule.source_ids or sourse_id in rule.source_ids:
                match, score = self._match_rule(rule, raw)
                if not match:
                    continue
                else:
                    return match, score

        return match, score

    def _match_rule(self, rule, raw) -> tuple[bool, int]:
        score = 0
        KEYWORDS = rule.include_keywords
        STOP_WORDS = rule.exclude_keywords
        MIN_TEXT_LENGTH = rule.min_text_length
        content = raw.content.lower()
        title = raw.title.lower()

        if MIN_TEXT_LENGTH > len(content):
            return False, 0
        content_matched = [k for k in KEYWORDS if k.replace("_", " ").lower() in content]
        title_matched = [k for k in KEYWORDS if k.replace("_", " ").lower() in title]

        text = title + " " + content

        if not content_matched and not title_matched:
            return False, 0

        if STOP_WORDS:
            if any(k.lower() in text for k in STOP_WORDS):
                return False, 0

        score += 1 if content_matched else 0
        score += 2 if title_matched else 0
        score += 1 if raw.price_limit else 0
        score += 1 if raw.possible_price_limit else 0
        score += 1 if raw.url else 0
        score += 1 if raw.author else 0

        if score < rule.min_score:
            return False, 0

        return True, score

    def should_notify(self, raw, score):
        text = (raw.title + " " + raw.content).lower()
        for rule in self.rules:
            matched = [k for k in rule.keywords_for_notis if k.lower() in text]
            if matched and score > rule.min_score_for_notis:
                return True
        return False
