import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List

from backend.app.db.crud import is_already_saved
from backend.app.sources.types import RawSourceItem

logger = logging.getLogger(__name__)


def extract_nuxt_data(html: str) -> dict:
    match = re.search(r"window\.__NUXT_DATA__\s*=\s*(\{.*?\});", html, re.S)
    if not match:
        return {}

    raw_json = match.group(1)
    return json.loads(raw_json)


def parse_kwork_date(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)

    value = value.strip()

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    # fallback, если формат неожиданный
    return datetime.now(timezone.utc)


def _extract_json_object_after_key(html: str, key: str) -> Dict[str, Any]:
    """
    Находит в тексте '"<key>":{...}' и возвращает распарсенный JSON-объект {...}
    через балансировку скобок, без regex по .*?
    """
    needle = f'"{key}":'
    start = html.find(needle)
    if start == -1:
        raise RuntimeError(f'Не найден ключ "{key}" в HTML')

    # ищем первую '{' после '"key":'
    i = start + len(needle)
    while i < len(html) and html[i] not in "{":
        i += 1
    if i >= len(html) or html[i] != "{":
        raise RuntimeError(f'После ключа "{key}" не найдено начало JSON объекта "{{"')

    # теперь считываем объект по балансу фигурных скобок
    depth = 0
    in_string = False
    escape = False
    j = i

    while j < len(html):
        ch = html[j]

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    # включаем текущую '}'
                    obj_str = html[i : j + 1]
                    return json.loads(obj_str)

        j += 1

    raise RuntimeError(f'Не удалось дочитать JSON объект для ключа "{key}" до конца (скобки не сошлись)')


def parse_kwork_projects(html: str) -> List[Dict[str, Any]]:
    """
    Достаёт проекты Kwork со страницы /projects из wantsListData.pagination.data
    """
    wants_list_data = _extract_json_object_after_key(html, "wantsListData")

    pagination = wants_list_data.get("pagination") or {}
    items = pagination.get("data") or []

    result: List[Dict[str, Any]] = []

    for p in items:
        pid = p.get("id")
        if not pid:
            continue

        description = p.get("description", "").lower()

        result.append(
            {
                "id": pid,
                "title": (p.get("name") or "").strip(),
                "description": description,
                "price_limit": p.get("priceLimit"),
                "possible_price_limit": str(p.get("possiblePriceLimit")),
                "category_id": p.get("category_id"),
                "lang": p.get("lang"),
                "username": (p.get("user") or {}).get("username"),
                "user_id": (p.get("user") or {}).get("USERID"),
                "published_at": parse_kwork_date(p.get("date_active")),
                "expires_at": parse_kwork_date(p.get("date_expire")),
                "url": f"https://kwork.ru/projects/{pid}",
            }
        )

    return result


async def process_projects(projects: list[dict[str, Any]]) -> tuple[bool, list[RawSourceItem]]:
    stop_category = False
    items = []
    for project in projects:
        project_id = project.get("id") or project.get("wantId")
        if not project_id:
            continue

        external_id = f"kwork:{project_id}"
        if await is_already_saved(external_id):
            stop_category = True
            break

        items.append(
            RawSourceItem(
                external_id=external_id,
                title=project.get("title", ""),
                content=project.get("description", ""),
                author=f"kwork id:{project.get("user_id", "")} username: {project.get("username", "unknown")}",
                published_at=parse_kwork_date(project.get("date_create")),
                url=f"https://kwork.ru/projects/{project_id}",
                metadata={
                    "price_limit": project.get("price_limit"),
                    "possible_price_limit": project.get("possible_price_limit"),
                    "category_id": project.get("category_id"),
                    "expires_at": project.get("expires_at"),
                    "lang": project.get("lang"),
                },
            )
        )
    return stop_category, items
