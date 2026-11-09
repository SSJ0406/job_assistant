"""Jednowęzłowy przepływ LangGraph przekazujący pytania do Answer Agenta."""

# Przepływ oddziela kolejność wykonania agenta od kodu interfejsu i sesji.

from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph

from job_assistant.agents.base import Agent


class WorkflowState(TypedDict, total=False):
    """Opisuje dane rozmowy przekazywane do węzła Answer Agenta."""

    query: str
    history: List[Dict[str, Any]]
    answer: str
    agent_trace: List[str]
    warnings: List[str]


class AgentWorkflow:
    """Przekazuje każde pytanie użytkownika bezpośrednio do Answer Agenta."""

    def __init__(self, agent: Agent):
        # Jeden jawny węzeł utrzymuje prostą ścieżkę wykonania dla obecnego agenta.
        self.agent = agent
        builder = StateGraph(WorkflowState)
        builder.add_node("answer", self._answer)
        builder.add_edge(START, "answer")
        builder.add_edge("answer", END)
        self.graph = builder.compile()

    def invoke(self, query: str, history=None) -> Dict[str, Any]:
        """Generuje odpowiedź z użyciem opcjonalnej historii rozmowy."""
        # Kopia chroni listę historii interfejsu przed zmianami w przepływie.
        return self.graph.invoke({"query": query, "history": list(history or [])})

    def _answer(self, state: WorkflowState) -> WorkflowState:
        # Ślad i ostrzeżenia wracają, aby interfejs mógł pokazać je użytkownikowi.
        result = self.agent.run(
            user_input=state.get("query", ""),
            history=state.get("history", []),
        )
        response: WorkflowState = {
            "answer": result.content,
            "agent_trace": [self.agent.name],
            "warnings": [],
        }
        if result.warning:
            response["warnings"] = [result.warning]
        return response
