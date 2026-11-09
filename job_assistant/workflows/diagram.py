"""Eksport czytelnego diagramu skompilowanego grafu LangGraph."""

# Osobny eksport pozwala tworzyć diagramy bez wiązania wykonania przepływu z dyskiem.

from pathlib import Path
from typing import Any, Optional, Tuple


def export_graph_diagram(
    compiled_graph: Any,
    png_path: Path,
    mermaid_path: Optional[Path] = None,
) -> Tuple[Path, Path]:
    """Zapisuje diagram grafu jako PNG oraz źródło Mermaid.

    Źródło Mermaid jest zapisywane przed próbą renderowania PNG, dzięki czemu
    pozostaje dostępne także wtedy, gdy renderowanie przez usługę Mermaid schemat
    zawiedzie.
    """
    png_path = Path(png_path)
    mermaid_path = (
        Path(mermaid_path)
        if mermaid_path is not None
        else png_path.with_suffix(".mmd")
    )
    if png_path.resolve() == mermaid_path.resolve():
        raise ValueError("Ścieżki pliku PNG i źródła Mermaid muszą być różne.")

    graph_view = compiled_graph.get_graph()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    mermaid_path.parent.mkdir(parents=True, exist_ok=True)

    # Źródło Mermaid pozostaje, jeśli późniejsze tworzenie obrazu PNG zawiedzie.
    mermaid_path.write_text(graph_view.draw_mermaid(), encoding="utf-8")
    image_bytes = graph_view.draw_mermaid_png()
    if not isinstance(image_bytes, bytes):
        raise TypeError("Renderer LangGraph powinien zwrócić dane PNG jako bytes.")
    png_path.write_bytes(image_bytes)
    return png_path, mermaid_path
