import unittest
import json
import os
from ai_agent_logs.log_summary import LogSummary
from ai_agent_logs.log_parser import LogParser
from ai_agent_logs.log_types import LogType


class TestLogSummary(unittest.TestCase):
    def setUp(self):
        """Creates a LogParser and LogSummary instance before each test."""
        self.parser = LogParser()
        self.summary = LogSummary(self.parser)

        # Simulated data
        self.parser.log_counts = {
            LogType.INFO: 3,
            LogType.ERROR: 2,
            LogType.WARNING: 1,
        }
        self.parser.agent_responses = {"Hello!": 2, "I don't understand.": 1}
        self.parser.error_messages = {"Model Timeout": 2}

    def test_display_results(self):
        """Tests the display function output."""
        with self.assertLogs(level="INFO") as log:
            self.summary.display_results()
        self.assertIn("Log Summary:", log.output[0])

    def test_save_results(self):
        """Tests saving results to a JSON file."""
        output_file = "data/test_log_summary.json"
        self.summary.save_results(output_file)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(data)
        self.assertEqual(data["log_summary"][LogType.INFO.value], 3)
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
