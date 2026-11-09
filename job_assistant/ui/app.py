"""Koordynacja uruchomienia i wyświetlania aplikacji Streamlit."""

# Osobny koordynator ułatwia zmianę kolejności widoku bez dotykania logiki agenta.

import streamlit as st

from job_assistant.agents.answer_agent import create_answer_agent
from job_assistant.agents.factory import AssistantFactory
from job_assistant.app_settings import AppSettings, load_settings
from job_assistant.ui.chat_controller import handle_user_input
from job_assistant.ui.components import (
    render_chat_history,
    render_configuration_warning,
    render_hero,
    render_welcome_card,
)
from job_assistant.ui.session_state import get_chat_messages, initialize_session_state
from job_assistant.ui.styles import apply_styles
from job_assistant.workflows.graph import AgentWorkflow


def configure_page() -> None:
    """Ustawia istniejące parametry strony Streamlit."""
    # Ustawiamy stronę jako pierwszą, bo Streamlit wymaga tego przed renderowaniem.
    st.set_page_config(
        page_title="Asystent ofert pracy",
        page_icon="💼",
        layout="centered",
    )


# Agent i przepływ są współdzielone, aby nie tworzyć ich przy każdym uruchomieniu.
# Pamięć zasobu obejmuje też inne sesje, jak w dotychczasowym działaniu.
@st.cache_resource
def get_app_components() -> tuple[AppSettings, AgentWorkflow]:
    """Tworzy współdzielone ustawienia i przepływ aplikacji."""
    # Składamy zależności tu, by kontroler interfejsu nie musiał konfigurować agenta.
    settings = load_settings()
    factory = AssistantFactory(settings=settings)
    workflow = AgentWorkflow(create_answer_agent(factory))
    return settings, workflow


def run_app() -> None:
    """Konfiguruje stronę i koordynuje renderowanie aplikacji."""
    configure_page()
    apply_styles()

    # Zachowujemy tę kolejność, aby historia sesji była gotowa przed pobraniem zasobów.
    initialize_session_state()
    settings, workflow = get_app_components()

    render_hero()
    render_configuration_warning(settings)

    chat_messages = get_chat_messages()
    if not chat_messages:
        render_welcome_card()

    render_chat_history(chat_messages)

    prompt = st.chat_input("Napisz wiadomość")
    if prompt:
        handle_user_input(workflow, prompt)
        # Ponowne wykonanie odświeża widok z wiadomościami dopisanymi przez kontroler.
        st.rerun()
