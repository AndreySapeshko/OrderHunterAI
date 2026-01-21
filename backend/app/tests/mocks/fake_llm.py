class FakeLLMClient:
    client_id = "fake_client"
    prompt = "fake prompt"

    def __init__(self, response: dict):
        self.response = response
        self.model = "fake-model"

    async def analyze(self, messages):
        return self.response


def get_fake_client(response=None):
    if response is None:
        response = {"fake response": "response"}
    return FakeLLMClient(response)
