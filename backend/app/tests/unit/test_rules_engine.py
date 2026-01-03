from backend.app.db.models.user_rule import UserRule
from backend.app.rules.engine import RuleEngine


async def test_rule_min_score_pass(raw_item, user_lead, user, session):
    rule = UserRule(user_id=user.id, min_score_for_notis=5, keyword_for_notis="test")
    user_lead.score = 7
    session.add(rule, user_lead)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.should_notify(raw_item, user_lead.score) is True


async def test_rule_min_score_fail(raw_item, user_lead, user, session):
    rule = UserRule(user_id=user.id, min_score_for_notis=5, keyword_for_notis="test")
    user_lead.score = 3
    session.add(rule, user_lead)
    await session.flush()
    engine = RuleEngine(
        [
            rule,
        ]
    )

    assert engine.should_notify(raw_item, user_lead.score) is False


async def test_rule_include_keywords_pass(raw_item, user, session):
    rule = UserRule(user_id=user.id, include_keywords=["test", "gpt"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(raw_item) == (True, 3)


async def test_rule_include_keywords_fail(raw_item, user, session):
    rule = UserRule(user_id=user.id, include_keywords=["voice"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(raw_item) == (False, 0)


async def test_rule_exclude_keywords_pass(raw_item, user, session):
    rule = UserRule(user_id=user.id, exclude_keywords=["blockchain"], include_keywords=["test"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(raw_item) == (True, 3)


async def test_rule_exclude_keywords_fail(raw_item, user, session):
    rule = UserRule(user_id=user.id, exclude_keywords=["test"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(raw_item) == (False, 0)


async def test_rule_combined_conditions_pass(raw_item, user, session):
    rule = UserRule(user_id=user.id, include_keywords=["test"], exclude_keywords=["gpt"])
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(raw_item) == (True, 3)


async def test_rule_combined_conditions_fail(raw_item, user, session):
    rule = UserRule(user_id=user.id, include_keywords=["chatbot"], exclude_keywords=["test"])  # не проходит
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(raw_item) == (False, 0)


async def test_disabled_rule_is_ignored(raw_item, user, session):
    rule = UserRule(user_id=user.id, include_keywords=["test"], enabled=False)
    session.add(rule)
    await session.flush()
    engine = RuleEngine([rule])

    assert engine.match(raw_item) == (True, 0)
