from backend.app.db.models.user_rule import UserRule
from backend.app.rules.engine import RuleEngine


async def test_rule_min_score_pass(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, min_score=70)
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is True


async def test_rule_min_score_fail(lead, lead_ai_bad_score, session):
    rule = UserRule(user_id=1, min_score=70)
    session.add(rule)
    await session.flush()
    engine = RuleEngine(
        [
            rule,
        ]
    )

    assert engine.match(lead, lead_ai_bad_score) is False


async def test_rule_category_pass(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, categories=["chatbot"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is True


async def test_rule_category_fail(lead, lead_ai_wrong_category, session):
    rule = UserRule(user_id=1, categories=["chatbot"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_wrong_category) is False


async def test_rule_include_keywords_pass(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, include_keywords=["chatbot", "gpt"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is True


async def test_rule_include_keywords_fail(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, include_keywords=["voice"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is False


async def test_rule_exclude_keywords_pass(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, exclude_keywords=["blockchain"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is True


async def test_rule_exclude_keywords_fail(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, exclude_keywords=["support"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is False


async def test_rule_combined_conditions_pass(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, min_score=70, categories=["chatbot"], include_keywords=["gpt"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is True


async def test_rule_combined_conditions_fail(lead, lead_ai_good, session):
    rule = UserRule(user_id=1, min_score=90, categories=["chatbot"], include_keywords=["gpt"])  # не проходит
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_good) is False


async def test_disabled_rule_is_ignored(lead, lead_ai_bad_score, session):
    rule = UserRule(user_id=1, min_score=100, enabled=False)
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(lead, lead_ai_bad_score) is True
