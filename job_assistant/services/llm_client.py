"""Adapter OpenAI Responses API udostępniający klienta agentom."""

# Mapowanie do dostawcy API pozostaje poza Agentem, by oddzielić logikę od integracji.

from typing import Dict, List

from job_assistant.agents.agent_config import AgentConfig


class OpenAIResponsesClient:
    """Dostosowuje OpenAI Responses API do interfejsu generate używanego przez agenta."""

    def __init__(self, client, config: AgentConfig):
        self._client = client
        self._config = config

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """Wysyła instrukcję systemową i historię rozmowy do Responses API."""
        # Agent zawsze przekazuje instrukcję jako pierwszą wiadomość systemową.
        if not messages or messages[0].get("role") != "system":
            raise ValueError("Agent messages must start with a system prompt.")

        request = {
            "model": self._config.model_name,
            "instructions": messages[0]["content"],
            "input": messages[1:],
            "max_output_tokens": self._config.max_output_tokens,
            "reasoning": {"effort": self._config.reasoning_effort},
            "store": False,
        }
        if self._config.reasoning_effort == "none":
            request["temperature"] = self._config.temperature

        response = self._client.responses.create(**request)
        output = getattr(response, "output_text", None)
        # Walidacja chroni dalsze etapy przed pustym albo nietekstowym wynikiem API.
        if not isinstance(output, str) or not output.strip():
            raise ValueError("The model did not return a text response.")
        return output
