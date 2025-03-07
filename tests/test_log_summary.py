import json
import os
import unittest

from ai_agent_logs.log_parser import LogParser
from ai_agent_logs.log_summary import LogSummary
from ai_agent_logs.log_types import LogType


class TestLogSummary(unittest.TestCase):
    """Tests the LogSummary functionality."""

    def setUp(self):
        """Initialize LogSummary with a mocked LogParser."""
        self.mock_parser = LogParser()
        self.mock_parser.log_counts = {
            LogType.INFO: 3,
            LogType.ERROR: 2,
            LogType.WARNING: 1,
        }
        self.mock_parser.agent_responses = {"Hello!": 2, "I don't understand.": 1}
        self.mock_parser.error_messages = {"Model Timeout": 2}

        self.summary = LogSummary(self.mock_parser)

    def test_display_results(self):
        """Tests if log summary results are correctly displayed."""
        with self.assertLogs(level="INFO") as log:
            self.summary.display_results()

        log_output = "\n".join(log.output)
        self.assertIn("INFO messages: 3", log_output)
        self.assertIn("ERROR messages: 2", log_output)
        self.assertIn("WARNING messages: 1", log_output)
        self.assertIn('"Hello!": 2', log_output)

    def test_save_results(self):
        """Tests saving results to a JSON file."""
        output_file = "output/test_log_summary.json"
        self.summary.save_results(output_file)

        self.assertTrue(os.path.exists(output_file))

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["log_summary"]["INFO"], 3)
        self.assertEqual(data["log_summary"]["ERROR"], 2)
        self.assertEqual(data["log_summary"]["WARNING"], 1)
        self.assertEqual(data["common_errors"]["Model Timeout"], 2)
        self.assertEqual(data["top_responses"]["Hello!"], 2)

        # Clean up test file
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
