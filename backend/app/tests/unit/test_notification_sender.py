from unittest.mock import AsyncMock, patch

import pytest

from backend.app.workers.tasks import notification_sender


@pytest.mark.asyncio
async def test_notification_sent_for_matching_user(lead, lead_ai_relevant, user, rule):
    items = [{"user": user, "rules": [rule]}]

    with (
        patch("backend.app.workers.tasks.get_all_active_users_with_rules", return_value=items),
        patch("backend.app.workers.tasks.get_notified_user_ids", return_value=set()),
        patch("backend.app.workers.tasks.create_lead_notification", new_callable=AsyncMock),
        patch("backend.app.workers.tasks.notify_lead", new_callable=AsyncMock),
        patch("backend.app.workers.tasks.RuleEngine.match", return_value=True),
    ):
        await notification_sender(lead, lead_ai_relevant)


@pytest.mark.asyncio
async def test_notification_not_sent_twice(lead, lead_ai_relevant, user, rule):
    items = [{"user": user, "rules": [rule]}]

    with (
        patch("backend.app.workers.tasks.get_all_active_users_with_rules", return_value=items),
        patch("backend.app.workers.tasks.get_notified_user_ids", return_value={user.id}),
        patch("backend.app.workers.tasks.create_lead_notification", new_callable=AsyncMock) as create_mock,
        patch("backend.app.workers.tasks.notify_lead", new_callable=AsyncMock) as notify_mock,
        patch("backend.app.workers.tasks.RuleEngine.match", return_value=True),
    ):
        await notification_sender(lead, lead_ai_relevant)

        create_mock.assert_not_awaited()
        notify_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_notification_blocked_by_rules(lead, lead_ai_relevant, user, rule):
    items = [{"user": user, "rules": [rule]}]

    with (
        patch("backend.app.workers.tasks.get_all_active_users_with_rules", return_value=items),
        patch("backend.app.workers.tasks.get_notified_user_ids", return_value=set()),
        patch("backend.app.workers.tasks.create_lead_notification", new_callable=AsyncMock) as create_mock,
        patch("backend.app.workers.tasks.notify_lead", new_callable=AsyncMock) as notify_mock,
        patch("backend.app.workers.tasks.RuleEngine.match", return_value=False),
    ):
        await notification_sender(lead, lead_ai_relevant)

        create_mock.assert_not_awaited()
        notify_mock.assert_not_awaited()
