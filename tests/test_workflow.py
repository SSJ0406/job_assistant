# Atrapa modelu pozwala sprawdzić przebieg bez wywołań do OpenAI.
import unittest

from job_assistant.agents.answer_agent import create_answer_agent
from job_assistant.agents.factory import AssistantFactory
from job_assistant.app_settings import load_settings
from job_assistant.workflows.graph import AgentWorkflow


class RecordingLLM:
    """Atrapa klienta zapisująca wiadomości bez wywoływania API."""

    def __init__(self):
        self.messages = None

    def generate(self, messages):
        self.messages = messages
        return "Odpowiedź testowa."


# Test chroni kontrakt historii i potwierdza bezpośrednią ścieżkę do Answer Agenta.
class WorkflowTests(unittest.TestCase):
    """Sprawdza dane przekazane przez przepływ do agenta."""

    def test_query_and_history_go_directly_to_answer_agent(self):
        llm = RecordingLLM()
        factory = AssistantFactory(
            settings=load_settings({"OPENAI_MODEL": "gpt-6-luna"}),
            llm_client=llm,
        )
        workflow = AgentWorkflow(create_answer_agent(factory))
        history = [{"role": "user", "content": "Pytanie z historii"}]

        result = workflow.invoke("Szukaj ofert pracy", history=history)

        self.assertEqual(result["answer"], "Odpowiedź testowa.")
        self.assertEqual(result["agent_trace"], ["Answer Agent"])
        self.assertEqual(result["warnings"], [])
        self.assertEqual(llm.messages[0]["role"], "system")
        self.assertIn("asystentem technicznym", llm.messages[0]["content"])
        self.assertEqual(llm.messages[-2], history[0])
        self.assertEqual(llm.messages[-1], {"role": "user", "content": "Szukaj ofert pracy"})


if __name__ == "__main__":
    unittest.main()
