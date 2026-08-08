import os
from typing import Any

import httpx

from .base import AIProvider


class RealAIProvider(AIProvider):
    """Real external AI teacher provider."""

    async def generate(
        self,
        message: str,
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        api_key = os.getenv("AI_API_KEY", "").strip()
        endpoint = os.getenv("AI_API_ENDPOINT", "").strip()

        if not api_key:
            raise RuntimeError("AI_API_KEY is not configured")

        if not endpoint:
            raise RuntimeError("AI_API_ENDPOINT is not configured")

        payload = {
            "message": message,
            "conversation_id": conversation_id,
            "context": context or {},
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                endpoint,
                json=payload,
                headers=headers,
            )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            for key in ("reply", "message", "response", "text"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()

        raise RuntimeError("AI provider returned an invalid response")
