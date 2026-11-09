"""Wczytuje ustawienia aplikacji ze zmiennych środowiskowych i pliku .env."""

# Jedno źródło konfiguracji zapobiega rozbieżnościom między agentem i interfejsem.

import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Mapping, Optional

from job_assistant.agents.agent_config import ANSWER_AGENT_CONFIG, AgentConfig


PROJECT_ROOT = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env", override=False)
except ImportError:
    # Aplikacja działa też w trybie lokalnym, gdy python-dotenv nie jest zainstalowany.
    pass


@dataclass(frozen=True)
class AppSettings:
    """Przechowuje dane połączenia OpenAI i ustawienia modelu agenta."""

    api_key: Optional[str]
    base_url: Optional[str]
    agent_config: AgentConfig

    @property
    def llm_enabled(self) -> bool:
        return bool(self.api_key)


def load_settings(environ: Optional[Mapping[str, str]] = None) -> AppSettings:
    """Wczytuje ustawienia agenta; klucz API jest opcjonalny w trybie awaryjnym."""
    env = os.environ if environ is None else environ
    model_name = env.get("OPENAI_MODEL", ANSWER_AGENT_CONFIG.model_name).strip()
    agent_config = replace(
        ANSWER_AGENT_CONFIG,
        model_name=model_name or ANSWER_AGENT_CONFIG.model_name,
    )
    return AppSettings(
        api_key=env.get("OPENAI_API_KEY", "").strip() or None,
        base_url=env.get("OPENAI_BASE_URL", "").strip() or None,
        agent_config=agent_config,
    )
