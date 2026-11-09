"""Podstawowe klasy Answer Agenta i budowania kontekstu rozmowy."""

# Wspólne reguły kontekstu i parsowania są oddzielone od klienta modelu i interfejsu.

import logging
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from job_assistant.agents.agent_config import AgentConfig


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class AgentRunResult:
    """Przechowuje odpowiedź agenta i opcjonalne ostrzeżenie o błędzie modelu."""

    content: str
    warning: Optional[str] = None


# Limit historii zostawia miejsce na instrukcję i bieżące pytanie w budżecie modelu.
class ContextManager:
    """Ogranicza historię rozmowy do skonfigurowanego budżetu kontekstu."""

    def __init__(self, max_context_tokens: int = 8000, max_history_messages: int = 12):
        self.max_context_tokens = max(1, int(max_context_tokens))
        self.max_history_messages = max(0, int(max_history_messages))

    def build_context(
        self,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict[str, str]]:
        """Zwraca ostatnie poprawne wiadomości z historii rozmowy."""
        messages = []
        if not self.max_history_messages:
            return messages
        for item in (history or [])[-self.max_history_messages:]:
            # Odrzucamy role i treści, których format rozmowy modelu nie obsługuje.
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and isinstance(content, str) and content.strip():
                messages.append({"role": role, "content": content.strip()})
        return messages

    @staticmethod
    def _estimate_tokens(message: Dict[str, str]) -> int:
        # Przybliżenie znaków wystarcza do kontroli limitu bez dodatkowego tokenizera.
        return (len(message.get("content", "")) + 3) // 4

    def fit_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Przycina historię, zachowując instrukcję systemową i bieżące pytanie."""
        if not messages:
            return messages
        if sum(self._estimate_tokens(message) for message in messages) <= self.max_context_tokens:
            return messages

        # Instrukcja systemowa i bieżące pytanie są ważniejsze niż najstarsza historia.
        first = dict(messages[0])
        last = dict(messages[-1])
        user_tokens = self._estimate_tokens(last)
        if user_tokens >= self.max_context_tokens:
            user_budget = max(
                0,
                self.max_context_tokens - max(1, self.max_context_tokens // 4),
            )
            last["content"] = self._truncate_content(last["content"], user_budget, from_end=True)
            user_tokens = self._estimate_tokens(last)

        system_budget = max(1, self.max_context_tokens - user_tokens)
        if self._estimate_tokens(first) > system_budget:
            first["content"] = self._truncate_content(
                first["content"], system_budget, marker=" [prompt skrócony]"
            )

        remaining = max(
            0,
            self.max_context_tokens - self._estimate_tokens(first) - user_tokens,
        )
        kept = []
        for message in reversed(messages[1:-1]):
            message = dict(message)
            needed = self._estimate_tokens(message)
            if needed <= remaining:
                kept.append(message)
                remaining -= needed
                continue
            if remaining:
                message["content"] = self._truncate_content(
                    message["content"], remaining, marker=" [kontekst skrócony]"
                )
                kept.append(message)
            break

        return [first, *reversed(kept), last]

    @staticmethod
    def _truncate_content(
        content: str,
        token_budget: int,
        marker: str = "",
        from_end: bool = False,
    ) -> str:
        # Skracamy treść, by zachować część kontekstu zamiast usuwać całą wiadomość.
        text = str(content)
        character_budget = max(0, token_budget) * 4
        if len(text) <= character_budget:
            return text
        if character_budget <= len(marker):
            if from_end and character_budget:
                return text[-character_budget:]
            return text[:character_budget]

        content_budget = character_budget - len(marker)
        if from_end:
            return marker + text[-content_budget:]
        return text[:content_budget] + marker


# Jedna walidacja obejmuje odpowiedź modelu i tryb awaryjny, by interfejs dostał tekst.
class OutputParser:
    """Waliduje tekstową odpowiedź modelu i usuwa białe znaki na brzegach."""

    @staticmethod
    def parse(response: str) -> str:
        if not isinstance(response, str):
            raise TypeError("Odpowiedź modelu musi być tekstem.")
        return response.strip()


class Agent:
    """Buduje wiadomości modelu i obsługuje odpowiedź lub lokalny tryb awaryjny."""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm,
        context_manager: ContextManager,
        fallback: Optional[Callable[[str], str]] = None,
        few_shot_examples: Optional[List[Dict[str, str]]] = None,
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm
        self.context_manager = context_manager
        self.fallback = fallback
        self.few_shot_examples = list(few_shot_examples or [])
        self.output_parser = OutputParser()

    def run(
        self,
        user_input: str,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> AgentRunResult:
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.few_shot_examples,
            *self.context_manager.build_context(history),
            {"role": "user", "content": user_input},
        ]
        messages = self.context_manager.fit_messages(messages)

        if self.llm is None:
            # Agent działa też bez klucza, dlatego zwraca lokalną odpowiedź awaryjną.
            return AgentRunResult(content=self._fallback_response(user_input))

        try:
            response = self.llm.generate(messages)
            return AgentRunResult(content=self.output_parser.parse(response))
        except Exception as exc:
            # Odpowiedź awaryjna podtrzymuje czat; ostrzeżenie informuje o awarii.
            LOGGER.exception(
                "Wywołanie modelu dla %s nie powiodło się (%s).",
                self.name,
                type(exc).__name__,
            )
            return AgentRunResult(
                content=self._fallback_response(user_input),
                warning=(
                    f"Wywołanie modelu {self.name} nie powiodło się "
                    f"({type(exc).__name__}); użyto lokalnej odpowiedzi."
                ),
            )

    def _fallback_response(self, user_input: str) -> str:
        response = self.fallback(user_input) if self.fallback else ""
        return self.output_parser.parse(response)
