import os


def get_ai_provider_name() -> str:
    return os.getenv("AI_PROVIDER", "echo").strip().lower() or "echo"
