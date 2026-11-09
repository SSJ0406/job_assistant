"""Typy wiadomości i dostęp do historii przechowywanej przez Streamlit."""

# Stan sesji zachowuje rozmowę, bo Streamlit ponownie wykonuje skrypt po interakcji.

from typing import Literal, NotRequired, TypedDict

import streamlit as st


# Metadane są opcjonalne, bo nie każda wiadomość jest odpowiedzią agenta.
class ChatMessage(TypedDict):
    """Opisuje wiadomość rozmowy zapisywaną w stanie sesji Streamlit."""

    role: Literal["user", "assistant"]
    content: str
    agent_trace: NotRequired[list[str]]
    warning: NotRequired[str | None]


def initialize_session_state() -> None:
    """Inicjalizuje historię rozmowy dla bieżącej sesji."""
    # Sprawdzenie klucza zapobiega utracie rozmowy przy każdym ponownym wykonaniu skryptu.
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []


def get_chat_messages() -> list[ChatMessage]:
    """Zwraca historię rozmowy bieżącej sesji."""
    # Mutacja tej listy zapisuje wiadomości bez osobnej synchronizacji stanu.
    return st.session_state.chat_messages
