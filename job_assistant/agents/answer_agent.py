"""Konfiguracja jedynego agenta dostępnego bezpośrednio dla użytkownika."""

# Instrukcje i przykłady są tu zebrane, by interfejs nie znał szczegółów agenta.

from job_assistant.agents.base import Agent
from job_assistant.agents.factory import AssistantFactory
from job_assistant.agents.prompts import ANSWER_AGENT_EXAMPLES, ANSWER_AGENT_PROMPT


ANSWER_AGENT_NAME = "Answer Agent"


def _fallback_response(_query: str) -> str:
    """Zwraca komunikat używany, gdy agent nie może wygenerować odpowiedzi."""
    # Tryb lokalny pozwala odpowiedzieć także wtedy, gdy klucz API nie jest dostępny.
    return (
        "Nie udało się uzyskać odpowiedzi z modelu. Sprawdź klucz "
        "OPENAI_API_KEY w pliku .env oraz połączenie z API, a potem spróbuj ponownie."
    )


def create_answer_agent(factory: AssistantFactory) -> Agent:
    """Tworzy Answer Agenta z fabryki i wspólnej instrukcji systemowej."""
    # Fabryka dostarcza klienta i kontekst, więc agent nie zależy od interfejsu.
    return factory.create_agent(
        name=ANSWER_AGENT_NAME,
        system_prompt=ANSWER_AGENT_PROMPT,
        fallback=_fallback_response,
        few_shot_examples=ANSWER_AGENT_EXAMPLES,
    )
