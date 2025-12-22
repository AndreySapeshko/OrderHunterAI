from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.registry import SourceRegistry


class RegistryTestConnector(BaseSourceConnector):
    source_id = "registry_test"
    source_name = "Registry Test"

    async def fetch(self, *, since=None, cursor=None, limit=100):
        return []


def test_source_registry_register_and_get() -> None:
    SourceRegistry.register(RegistryTestConnector)

    connector_cls = SourceRegistry.get("registry_test")

    assert connector_cls is RegistryTestConnector
    assert "registry_test" in SourceRegistry.list_sources()
