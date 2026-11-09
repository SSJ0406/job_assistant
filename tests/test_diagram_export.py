"""Testy zapisu diagramu bez zależności od mechanizmu tworzenia obrazu LangGraph."""

# Atrapy dają powtarzalne pliki i nie wymagają zewnętrznej usługi renderującej.

import tempfile
import unittest
from pathlib import Path

from job_assistant.workflows.diagram import export_graph_diagram


# Testy korzystają z małych atrap, by sprawdzić zapisywanie plików i ścieżki błędów.
class FakeGraphView:
    """Minimalny zamiennik widoku grafu używany przez testy eksportu."""

    def draw_mermaid(self):
        """Zwraca deterministyczne źródło diagramu."""
        return "graph TD\n    START --> answer\n    answer --> END\n"

    def draw_mermaid_png(self):
        """Zwraca stałe bajty imitujące obraz PNG."""
        return b"fake-png"


class FakeCompiledGraph:
    """Udostępnia widok grafu przez metodę zgodną z LangGraph."""

    def get_graph(self):
        """Zwraca widok grafu testowego."""
        return FakeGraphView()


class DiagramExportTests(unittest.TestCase):
    """Regresje eksportu plików PNG i Mermaid."""

    # Źródło Mermaid zapisuje się przed obrazem, więc testujemy błąd jego tworzenia.
    def test_exports_png_and_mermaid_source(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            png_path = Path(temporary_directory) / "nested" / "graph.png"

            saved_png, saved_mermaid = export_graph_diagram(FakeCompiledGraph(), png_path)

            self.assertEqual(saved_png.read_bytes(), b"fake-png")
            self.assertEqual(saved_mermaid, png_path.with_suffix(".mmd"))
            self.assertIn("START --> answer", saved_mermaid.read_text(encoding="utf-8"))

    # Źródło Mermaid musi pozostać dostępne, nawet gdy tworzenie obrazu zgłosi błąd.
    def test_keeps_mermaid_source_when_png_rendering_fails(self):
        class BrokenGraphView(FakeGraphView):
            def draw_mermaid_png(self):
                raise RuntimeError("renderer unavailable")

        class BrokenCompiledGraph:
            def get_graph(self):
                return BrokenGraphView()

        with tempfile.TemporaryDirectory() as temporary_directory:
            png_path = Path(temporary_directory) / "graph.png"

            with self.assertRaises(RuntimeError):
                export_graph_diagram(BrokenCompiledGraph(), png_path)

            self.assertTrue(png_path.with_suffix(".mmd").exists())
            self.assertFalse(png_path.exists())

    # Walidacja ścieżek chroni istniejące pliki przed przypadkowym nadpisaniem.
    def test_rejects_identical_output_paths_before_overwriting(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "graph.png"
            output_path.write_bytes(b"existing file")

            with self.assertRaises(ValueError):
                export_graph_diagram(
                    FakeCompiledGraph(), output_path, mermaid_path=output_path
                )

            self.assertEqual(output_path.read_bytes(), b"existing file")


if __name__ == "__main__":
    unittest.main()
