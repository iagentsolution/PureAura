from __future__ import annotations

from application.contracts.ai import AIProvider
from config import settings

from .groq_provider import GroqProvider


class AIProviderFactory:
    def create(self) -> AIProvider:
        return GroqProvider.from_api_key(
            api_key=settings.groq.api_key,
            model=settings.groq.model,
        )


_provider_factory = AIProviderFactory()


def create_ai_provider() -> AIProvider:
    return _provider_factory.create()


__all__ = [
    "AIProviderFactory",
    "create_ai_provider",
]