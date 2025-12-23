from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    async def analyze(self, messages: list[dict]) -> dict:
        raise NotImplementedError
