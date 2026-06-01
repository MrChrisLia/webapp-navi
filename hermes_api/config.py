"""Environment-driven configuration. No hardcoded paths (design rule 6/7)."""
import os


class Settings:
    provider: str = os.getenv("HERMES_PROVIDER", "mock")
    base_url: str = os.getenv("HERMES_BASE_URL", "")
    model: str = os.getenv("HERMES_MODEL", "")
    api_key: str = os.getenv("HERMES_API_KEY", "")
    db_path: str = os.getenv("HERMES_DB_PATH", "hermes_api/data/hermes.sqlite")


settings = Settings()
