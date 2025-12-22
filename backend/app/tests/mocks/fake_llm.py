class FakeLLMClient:
    def __init__(self, response: dict):
        self.response = response
        self.model = "fake-model"

    async def analyze(self, messages):
        return self.response
