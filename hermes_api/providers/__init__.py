"""LLM provider abstraction. Selected via HERMES_PROVIDER env var."""
from hermes_api.config import settings
from hermes_api.providers.base import LLMProvider
from hermes_api.providers.mock import MockProvider
from hermes_api.providers.openai_compatible import OpenAICompatibleProvider


def get_provider() -> LLMProvider:
    name = settings.provider.lower()
    if name in {"openai_compatible", "openai-compatible", "hermes_agent", "hermes-agent"}:
        return OpenAICompatibleProvider()
    if name == "mock":
        return MockProvider()
    # Unknown providers fall back to mock so the service always starts.
    return MockProvider()
