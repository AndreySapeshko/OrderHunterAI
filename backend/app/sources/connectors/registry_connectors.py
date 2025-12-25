from backend.app.sources.connectors.reddit_forhire import RedditForHireConnector
from backend.app.sources.registry import SourceRegistry

SourceRegistry.register(RedditForHireConnector)
