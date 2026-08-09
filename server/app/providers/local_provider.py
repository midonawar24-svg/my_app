from typing import Any

from app.services.local_ai_config import LocalAIConfig
from app.services.local_ai_runner import LocalAIRunner

from .base import AIProvider


class LocalAIProvider(AIProvider):
    """Local GGUF AI provider backed by llama.cpp."""

    def __init__(
        self,
        config: LocalAIConfig | None = None,
    ):
        self.config = config or LocalAIConfig.from_env()
        self.runner = LocalAIRunner(self.config)

    def _select_model(self):
        models = sorted(self.config.models_dir.glob("*.gguf"))

        if not models:
            raise RuntimeError(
                f"No GGUF models found in {self.config.models_dir}"
            )

        return models[0]

    async def generate(
        self,
        message: str,
        conversation_id: str = "",
        context: dict[str, Any] | None = None,
    ) -> str:
        model = self._select_model()

        prompt = message

        if context:
            prompt = (
                "Context:\n"
                f"{context}\n\n"
                "User request:\n"
                f"{message}"
            )

        return await self.runner.generate(
            model=model,
            prompt=prompt,
            max_tokens=512,
        )
