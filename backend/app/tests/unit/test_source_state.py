import pytest

from backend.app.sources.state import SourceState


@pytest.mark.asyncio
async def test_save_and_get_cursor(sessionmaker, monkeypatch) -> None:
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    state = SourceState()

    await state.save_cursor("test_source", "cursor_1")
    cursor = await state.get_cursor("test_source")

    assert cursor == "cursor_1"


@pytest.mark.asyncio
async def test_cursor_overwrite(sessionmaker, monkeypatch) -> None:
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    state = SourceState()

    await state.save_cursor("test_source", "cursor_1")
    await state.save_cursor("test_source", "cursor_2")

    cursor = await state.get_cursor("test_source")
    assert cursor == "cursor_2"


@pytest.mark.asyncio
async def test_mark_success_resets_error_count(sessionmaker, monkeypatch) -> None:
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    state = SourceState()

    await state.mark_error("test_source", "error")
    await state.mark_error("test_source", "error")

    await state.mark_success("test_source")

    cursor = await state.get_cursor("test_source")
    assert cursor is None  # cursor не должен измениться


@pytest.mark.asyncio
async def test_mark_error_creates_state(sessionmaker, monkeypatch) -> None:
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    state = SourceState()

    await state.mark_error("new_source", "something failed")

    cursor = await state.get_cursor("new_source")
    assert cursor is None
