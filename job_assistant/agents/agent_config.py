"""Ustawienia modelu i budżetu kontekstu Answer Agenta."""

# Konfigurację trzymamy poza kodem agenta, by parametry miały jedno źródło.

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    """Przechowuje nazwę modelu oraz jego parametry i limity kontekstu."""

    # Niemutowalność chroni ustawienia przed zmianą po wstrzyknięciu do agenta.

    model_name: str = "gpt-6-luna"
    temperature: float = 0
    max_output_tokens: int = 2000
    context_tokens: int = 8000
    reasoning_effort: str = "none"


ANSWER_AGENT_CONFIG = AgentConfig()
