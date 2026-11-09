"""Punkt wejścia uruchamiany poleceniem `streamlit run main.py`."""

# Mały plik startowy ułatwia testowanie interfejsu bez rozbudowy punktu wejścia.

from job_assistant.ui.app import run_app


if __name__ == "__main__":
    run_app()
