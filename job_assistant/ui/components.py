"""Funkcje renderujące elementy widoku aplikacji."""

# Osobne wyświetlanie pozwala zmieniać interfejs bez naruszania logiki agenta.

from collections.abc import Sequence

import streamlit as st

from job_assistant.app_settings import AppSettings
from job_assistant.ui.session_state import ChatMessage


def render_hero() -> None:
    """Wyświetla sekcję wprowadzającą do aplikacji."""
    # Osobna funkcja ułatwia zmiany wprowadzenia bez rozbudowy koordynatora.
    st.markdown(
        """
        <section class="career-hero">
            <div class="career-eyebrow">
                <span class="career-dot"></span> Asystent ofert pracy
            </div>
            <h1 class="career-title">Praca zaczyna się od dobrego pytania.</h1>
            <p class="career-copy">
                Porozmawiaj o ofertach, wymaganiach i serwisach rekrutacyjnych.
                Wklej treść ogłoszenia albo opisz, czego szukasz.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_configuration_warning(settings: AppSettings) -> None:
    """Wyświetla komunikat o braku konfiguracji API, jeśli model jest wyłączony."""
    # Informujemy o trybie lokalnym, żeby brak odpowiedzi z modelu nie był zaskoczeniem.
    if not settings.llm_enabled:
        st.info(
            "Brak klucza API. Dodaj OPENAI_API_KEY do pliku .env "
            "i uruchom aplikację ponownie."
        )


def render_welcome_card() -> None:
    """Wyświetla kartę powitalną przed rozpoczęciem rozmowy."""
    # Karta pomaga zacząć czat, a znika po pojawieniu się wiadomości.
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-icon">✦</div>
            <div>
                <p class="welcome-title">Od czego zaczynamy?</p>
                <p class="welcome-copy">
                    Zapytaj o portale z ofertami pracy lub wklej ogłoszenie,
                    które chcesz przeanalizować.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_message(message: ChatMessage) -> None:
    """Wyświetla jedną wiadomość i jej opcjonalne metadane."""
    # Metadane są opcjonalne, bo wiadomości użytkownika i błędów ich nie zawierają.
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("agent_trace"):
            st.caption("Agent: " + ", ".join(message["agent_trace"]))
        if message.get("warning"):
            st.warning(message["warning"])


def render_chat_history(messages: Sequence[ChatMessage]) -> None:
    """Wyświetla wszystkie wiadomości z przekazanej historii."""
    # Jedna ścieżka renderowania utrzymuje taki sam wygląd każdej wiadomości.
    for message in messages:
        render_chat_message(message)
