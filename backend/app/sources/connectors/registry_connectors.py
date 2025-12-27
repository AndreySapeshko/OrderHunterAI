from backend.app.sources.connectors.kwork_projects import KworkProjectsConnector

# from backend.app.sources.connectors.reddit_forhire import RedditForHireConnector
# from backend.app.sources.connectors.telegram_channel import TelegramChannelConnector
from backend.app.sources.registry import SourceRegistry

# SourceRegistry.register(RedditForHireConnector)
# SourceRegistry.register(TelegramChannelConnector)
SourceRegistry.register(KworkProjectsConnector)
