"""LLM provider abstraction. Selected via HERMES_PROVIDER env var."""
from hermes_api.config import settings
from hermes_api.providers.base import LLMProvider
from hermes_api.providers.mock import MockProvider


def get_provider() -> LLMProvider:
    name = settings.provider.lower()
    # Only the mock provider ships in the basic version; others are stubs later.
    if name == "mock":
        return MockProvider()
    # Unknown providers fall back to mock so the service always starts.
    return MockProvider()
