from backend.app.sources.registry import SourceRegistry
from backend.app.sources.connectors.reddit_forhire import RedditForHireConnector

SourceRegistry.register(RedditForHireConnector)
