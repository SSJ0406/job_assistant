"""Eksportuje strukturę przepływu aplikacji do graph.png i graph.mmd."""

# Oddzielne polecenie pozwala podejrzeć graf bez uruchamiania aplikacji Streamlit.

import argparse
import sys
from pathlib import Path

from job_assistant.agents.answer_agent import create_answer_agent
from job_assistant.agents.factory import AssistantFactory
from job_assistant.app_settings import load_settings
from job_assistant.workflows.diagram import export_graph_diagram
from job_assistant.workflows.graph import AgentWorkflow


def create_workflow():
    """Buduje graf jednego Answer Agenta bez wywołania modelu."""
    # Ta sama fabryka zapewnia zgodność diagramu z grafem używanym przez aplikację.
    factory = AssistantFactory(settings=load_settings())
    return AgentWorkflow(create_answer_agent(factory))


def main(argv=None):
    """Zapisuje PNG i źródło Mermaid z opcjonalnie wskazanych ścieżek."""
    parser = argparse.ArgumentParser(description="Eksport diagramu workflow agentów.")
    parser.add_argument("--output", type=Path, default=Path("graph.png"), help="Ścieżka pliku PNG.")
    parser.add_argument("--mermaid-output", type=Path, help="Opcjonalna ścieżka pliku .mmd.")
    arguments = parser.parse_args(argv)

    try:
        # Błąd eksportu zamieniamy na zwięzły komunikat i kod niepowodzenia terminala.
        workflow = create_workflow()
        png_path, mermaid_path = export_graph_diagram(
            workflow.graph,
            png_path=arguments.output,
            mermaid_path=arguments.mermaid_output,
        )
    except Exception as exc:
        print(
            "Nie udało się wyeksportować diagramu ({}).".format(
                type(exc).__name__
            ),
            file=sys.stderr,
        )
        return 1

    print("Zapisano diagram: {} oraz {}".format(png_path, mermaid_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
