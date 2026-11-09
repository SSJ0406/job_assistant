# Atrapa punktu końcowego pozwala sprawdzić konfigurację bez dostępu do API.
import unittest
from types import SimpleNamespace

from job_assistant.agents.agent_config import AgentConfig
from job_assistant.agents.factory import AssistantFactory
from job_assistant.app_settings import load_settings
from job_assistant.services.llm_client import OpenAIResponsesClient


# Zapisujemy żądanie zamiast wysyłać je do OpenAI, by test był deterministyczny.
class FakeResponsesEndpoint:
    def __init__(self, output_text="odpowiedź"):
        self.output_text = output_text
        self.request = None

    def create(self, **request):
        self.request = request
        return SimpleNamespace(output_text=self.output_text)


class FactoryTests(unittest.TestCase):
    """Sprawdza konfigurację fabryki i mapowanie żądań bez połączenia sieciowego."""

    # Jawne ustawienia chronią test przed przypadkowymi zmiennymi środowiska.
    def test_settings_use_model_and_fixed_answer_agent_options(self):
        settings = load_settings({
            "OPENAI_MODEL": "gpt-6-luna",
        })

        self.assertEqual(settings.agent_config.model_name, "gpt-6-luna")
        self.assertEqual(settings.agent_config.temperature, 0)
        self.assertEqual(settings.agent_config.max_output_tokens, 2000)
        self.assertEqual(settings.agent_config.context_tokens, 8000)
        self.assertEqual(settings.agent_config.reasoning_effort, "none")
        self.assertFalse(settings.llm_enabled)

    # Parametry modelu pozostają stałe, gdy nie są częścią publicznej konfiguracji.
    def test_agent_settings_are_not_read_from_environment(self):
        config = load_settings({
            "ANSWER_AGENT_TEMPERATURE": "0.5",
            "ANSWER_AGENT_MAX_TOKENS": "1200",
            "ANSWER_AGENT_CONTEXT_TOKENS": "4000",
            "ANSWER_AGENT_REASONING_EFFORT": "low",
        }).agent_config

        self.assertEqual(config.temperature, 0)
        self.assertEqual(config.max_output_tokens, 2000)
        self.assertEqual(config.context_tokens, 8000)
        self.assertEqual(config.reasoning_effort, "none")

    # Brak klucza ma aktywować tryb lokalny zamiast budować nieużywalnego klienta.
    def test_factory_uses_local_mode_without_api_key(self):
        agent = AssistantFactory(settings=load_settings({})).create_agent(
            name="Answer Agent",
            system_prompt="prompt",
            fallback=lambda query: "fallback",
        )

        self.assertIsNone(agent.llm)
        self.assertEqual(agent.context_manager.max_context_tokens, 8000)

    # Wstrzyknięcie klienta umożliwia testowanie agenta bez prawdziwego klienta API.
    def test_factory_accepts_injected_client(self):
        fake_client = object()
        settings = load_settings({"OPENAI_API_KEY": "test-key"})
        agent = AssistantFactory(settings=settings, llm_client=fake_client).create_agent(
            name="Answer Agent",
            system_prompt="prompt",
            fallback=lambda query: "fallback",
        )

        self.assertIs(agent.llm, fake_client)

    # Mapowanie żądania chroni zgodność parametrów modelu i wyłączonego przechowywania.
    def test_responses_adapter_maps_settings_and_disables_storage(self):
        endpoint = FakeResponsesEndpoint()
        adapter = OpenAIResponsesClient(
            SimpleNamespace(responses=endpoint),
            AgentConfig(model_name="gpt-6-luna"),
        )

        response = adapter.generate([
            {"role": "system", "content": "system prompt"},
            {"role": "user", "content": "pytanie"},
        ])

        self.assertEqual(response, "odpowiedź")
        self.assertEqual(endpoint.request["model"], "gpt-6-luna")
        self.assertEqual(endpoint.request["instructions"], "system prompt")
        self.assertEqual(endpoint.request["input"], [{"role": "user", "content": "pytanie"}])
        self.assertEqual(endpoint.request["max_output_tokens"], 2000)
        self.assertEqual(endpoint.request["reasoning"], {"effort": "none"})
        self.assertEqual(endpoint.request["temperature"], 0)
        self.assertFalse(endpoint.request["store"])

    # Bez komunikatu systemowego klient nie powinien wysyłać niepełnego żądania.
    def test_responses_adapter_requires_system_message(self):
        adapter = OpenAIResponsesClient(
            SimpleNamespace(responses=FakeResponsesEndpoint()),
            AgentConfig(model_name="gpt-6-luna"),
        )

        with self.assertRaises(ValueError):
            adapter.generate([{"role": "user", "content": "pytanie"}])


if __name__ == "__main__":
    unittest.main()
