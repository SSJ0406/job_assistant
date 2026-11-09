"""Obsługa zapytania użytkownika i wyniku zwróconego przez przepływ."""

# Wydzielenie kontrolera pozwala testować wynik i błędy bez uruchamiania interfejsu.

import logging

from job_assistant.ui.session_state import get_chat_messages
from job_assistant.workflows.graph import AgentWorkflow


LOGGER = logging.getLogger(__name__)


def handle_user_input(workflow: AgentWorkflow, prompt: str) -> None:
    """Wywołuje przepływ i dopisuje wiadomość użytkownika oraz odpowiedź."""
    # Interfejs przekazuje pytanie do przepływu, bo to on uruchamia Answer Agenta.
    chat_messages = get_chat_messages()
    # Przepływ dostaje wcześniejsze wpisy, bo bieżące pytanie przekazujemy osobno.
    previous_history = list(chat_messages)
    chat_messages.append({"role": "user", "content": prompt})
    try:
        result = workflow.invoke(query=prompt, history=previous_history)
        # Jedno ostrzeżenie zachowuje dotychczasowy format wpisu w historii.
        chat_messages.append({
            "role": "assistant",
            "content": result.get("answer", "Nie udało się przygotować odpowiedzi."),
            "agent_trace": result.get("agent_trace", []),
            "warning": (result.get("warnings") or [None])[0],
        })
    except Exception as exc:
        # Odpowiedź błędu pozwala kontynuować czat; logger zachowuje szczegóły.
        LOGGER.exception("Nie udało się obsłużyć wiadomości w workflow.")
        chat_messages.append({
            "role": "assistant",
            "content": (
                f"Nie udało się obsłużyć wiadomości ({type(exc).__name__}). "
                "Spróbuj ponownie."
            ),
        })
