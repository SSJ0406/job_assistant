"""Fabryka agentów i współdzielonych zależności modelu."""

# Fabryka oddziela konfigurację klienta modelu językowego od logiki agenta.

from typing import Dict, List, Optional

from job_assistant.agents.base import Agent, ContextManager
from job_assistant.app_settings import AppSettings, load_settings
from job_assistant.services.llm_client import OpenAIResponsesClient


class LLMConfigurationError(RuntimeError):
    """Sygnalizuje, że klient OpenAI nie może zostać poprawnie skonfigurowany."""


class AssistantFactory:
    """Tworzy agentów ze wspólnym klientem modelu i konfiguracją kontekstu."""

    def __init__(self, settings: Optional[AppSettings] = None, llm_client=None):
        # Wstrzyknięte zależności ułatwiają testy bez czytania środowiska i wywołań API.
        self.settings = settings or load_settings()
        self._llm_client = llm_client if llm_client is not None else self._build_openai_client()

    def create_agent(
        self,
        name: str,
        system_prompt: str,
        fallback,
        few_shot_examples: Optional[List[Dict[str, str]]] = None,
    ) -> Agent:
        return Agent(
            name=name,
            system_prompt=system_prompt,
            llm=self._llm_client,
            context_manager=ContextManager(self.settings.agent_config.context_tokens),
            fallback=fallback,
            few_shot_examples=few_shot_examples,
        )

    def _build_openai_client(self):
        # Bez klucza wybieramy tryb lokalny i unikamy nieużytego klienta API.
        if not self.settings.api_key:
            return None

        try:
            # Import jest odroczony, bo pakiet OpenAI jest potrzebny tylko przy kluczu.
            from openai import OpenAI
        except ImportError as exc:
            raise LLMConfigurationError(
                "The openai package is missing. Install dependencies from requirements.txt."
            ) from exc

        options = {"api_key": self.settings.api_key}
        if self.settings.base_url:
            options["base_url"] = self.settings.base_url
        return OpenAIResponsesClient(OpenAI(**options), self.settings.agent_config)
