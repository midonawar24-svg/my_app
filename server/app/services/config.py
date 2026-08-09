import os


def get_ai_provider_name() -> str:
    return os.getenv("AI_PROVIDER", "local").strip().lower() or "echo"
