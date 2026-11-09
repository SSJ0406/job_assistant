"""Testy jednostkowe obsługi wiadomości w interfejsie Streamlit."""

# Izolujemy zależności, aby testy nie wysyłały zapytań do modelu językowego.

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from job_assistant.ui.chat_controller import handle_user_input
from job_assistant.workflows.graph import AgentWorkflow


class ChatControllerTests(unittest.TestCase):
    # Wcześniejsza wiadomość ujawnia, czy kontroler zachowuje kontrakt historii.
    def setUp(self):
        self.chat_messages = [{"role": "assistant", "content": "Poprzednia odpowiedź"}]
        self.streamlit_mock = SimpleNamespace(
            session_state=SimpleNamespace(chat_messages=self.chat_messages)
        )

    def handle_input(self, workflow, prompt="Nowe pytanie"):
        # Atrapa omija zależność od aktywnego kontekstu Streamlit podczas testów.
        with patch("job_assistant.ui.session_state.st", self.streamlit_mock):
            handle_user_input(workflow, prompt)

    # Chroni przekazywanie poprzedniej historii i zachowanie metadanych odpowiedzi.
    def test_successful_response_uses_previous_history_and_stores_trace(self):
        workflow = Mock(spec=AgentWorkflow)
        workflow.invoke.return_value = {
            "answer": "Odpowiedź agenta",
            "agent_trace": ["Answer Agent"],
            "warnings": [],
        }

        self.handle_input(workflow)

        workflow.invoke.assert_called_once_with(
            query="Nowe pytanie",
            history=[{"role": "assistant", "content": "Poprzednia odpowiedź"}],
        )
        self.assertEqual(
            self.chat_messages[-2:],
            [
                {"role": "user", "content": "Nowe pytanie"},
                {
                    "role": "assistant",
                    "content": "Odpowiedź agenta",
                    "agent_trace": ["Answer Agent"],
                    "warning": None,
                },
            ],
        )

    # Odpowiedź domyślna utrzymuje czytelny komunikat przy niepełnym wyniku przepływu.
    def test_missing_answer_uses_existing_default_response(self):
        workflow = Mock(spec=AgentWorkflow)
        workflow.invoke.return_value = {"warnings": []}

        self.handle_input(workflow)

        self.assertEqual(
            self.chat_messages[-1]["content"],
            "Nie udało się przygotować odpowiedzi.",
        )

    # Pusta lista nie może wywołać błędu indeksowania ani pokazać pustego ostrzeżenia.
    def test_empty_warnings_store_no_warning(self):
        workflow = Mock(spec=AgentWorkflow)
        workflow.invoke.return_value = {"answer": "Odpowiedź", "warnings": []}

        self.handle_input(workflow)

        self.assertIsNone(self.chat_messages[-1]["warning"])

    # Ten przypadek utrwala obecną regułę wyboru pojedynczego ostrzeżenia.
    def test_first_workflow_warning_is_stored(self):
        workflow = Mock(spec=AgentWorkflow)
        workflow.invoke.return_value = {
            "answer": "Odpowiedź",
            "warnings": ["Pierwsze ostrzeżenie", "Drugie ostrzeżenie"],
        }

        self.handle_input(workflow)

        self.assertEqual(self.chat_messages[-1]["warning"], "Pierwsze ostrzeżenie")

    # Błąd przepływu nie powinien przerwać sesji ani zniknąć bez śladu w logu.
    def test_workflow_exception_is_logged_and_stored_as_existing_error_message(self):
        workflow = Mock(spec=AgentWorkflow)
        workflow.invoke.side_effect = RuntimeError("workflow failure")

        with self.assertLogs("job_assistant.ui.chat_controller", level="ERROR") as logs:
            self.handle_input(workflow)

        self.assertIn("Nie udało się obsłużyć wiadomości w workflow.", logs.output[0])
        self.assertEqual(
            self.chat_messages[-1],
            {
                "role": "assistant",
                "content": (
                    "Nie udało się obsłużyć wiadomości (RuntimeError). "
                    "Spróbuj ponownie."
                ),
            },
        )


if __name__ == "__main__":
    unittest.main()
