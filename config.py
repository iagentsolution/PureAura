from __future__ import annotations

from dataclasses import dataclass
import os


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True, slots=True)
class GroqConfig:
    api_key: str
    model: str
    temperature: float
    max_tokens: int
    timeout_seconds: float


@dataclass(frozen=True, slots=True)
class AppConfig:
    app_name: str
    app_version: str
    debug: bool
    groq: GroqConfig


def load_config() -> AppConfig:
    return AppConfig(
        app_name=_get_env("PUREAURA_APP_NAME", "PureAura"),
        app_version=_get_env("PUREAURA_APP_VERSION", "1.0.0"),
        debug=_get_env("PUREAURA_DEBUG", "false").lower() == "true",
        groq=GroqConfig(
            api_key=_get_env("GROQ_API_KEY"),
            model=_get_env("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=float(_get_env("GROQ_TEMPERATURE", "0.7")),
            max_tokens=int(_get_env("GROQ_MAX_TOKENS", "2048")),
            timeout_seconds=float(_get_env("GROQ_TIMEOUT", "60")),
        ),
    )


settings = load_config()