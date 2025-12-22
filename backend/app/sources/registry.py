from typing import Dict, Type

from backend.app.sources.base import BaseSourceConnector


class SourceRegistry:
    _registry: Dict[str, Type[BaseSourceConnector]] = {}

    @classmethod
    def register(cls, connector: Type[BaseSourceConnector]) -> None:
        cls._registry[connector.source_id] = connector

    @classmethod
    def get(cls, source_id: str) -> Type[BaseSourceConnector]:
        return cls._registry[source_id]

    @classmethod
    def list_sources(cls) -> list[str]:
        return list(cls._registry.keys())
