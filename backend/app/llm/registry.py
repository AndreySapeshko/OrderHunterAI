from typing import Dict

from backend.app.llm.client import BaseLLMClient


class ClientRegistry:
    _registry: Dict[str, BaseLLMClient] = {}

    @classmethod
    def register(cls, client: BaseLLMClient) -> None:
        cls._registry[client.client_id] = client

    @classmethod
    def get(cls, client_id: str) -> BaseLLMClient:
        return cls._registry[client_id]

    @classmethod
    def list_clients(cls) -> list[BaseLLMClient]:
        return list(cls._registry.values())

    @classmethod
    def list_client_names(cls) -> list[str]:
        return list(cls._registry.keys())
