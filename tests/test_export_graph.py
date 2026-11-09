# Testujemy obsługę błędów polecenia bez tworzenia grafu ani plików na dysku.
import io
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

from job_assistant.workflows.export_graph import main


class ExportGraphCommandTests(unittest.TestCase):
    """Sprawdza komunikat i kod wyjścia eksportu uruchamianego w terminalu."""

    # Błąd ma dać czytelny komunikat i kod niepowodzenia dla polecenia terminala.
    def test_reports_general_export_failure_when_workflow_creation_fails(self):
        error_output = io.StringIO()
        with patch(
            "job_assistant.workflows.export_graph.create_workflow",
            side_effect=RuntimeError("workflow unavailable"),
        ), redirect_stderr(error_output):
            result = main(["--output", "graph.png"])

        self.assertEqual(result, 1)
        self.assertIn(
            "Nie udało się wyeksportować diagramu (RuntimeError)",
            error_output.getvalue(),
        )
        self.assertNotIn("wygenerować PNG", error_output.getvalue())
