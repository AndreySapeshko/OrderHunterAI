from backend.app.llm.open_router_client import get_open_router_client
from backend.app.llm.openai_client import get_open_ai_client
from backend.app.llm.registry import ClientRegistry

ClientRegistry.register(get_open_ai_client())
ClientRegistry.register(get_open_router_client())
