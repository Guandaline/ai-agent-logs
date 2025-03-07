import unittest
from unittest.mock import mock_open, patch

from ai_agent_logs.log_parser import LogParser
from ai_agent_logs.log_types import LogType


class TestLogParser(unittest.TestCase):
    """Tests the LogParser functionality."""

    def setUp(self):
        """Initialize LogParser instance before each test."""
        self.parser = LogParser()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            '[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"\n'
            "[2025-02-20 14:33:00] ERROR - Model Timeout\n"
            "[2025-02-20 14:34:20] WARNING - Possible delay detected\n"
        ),
    )
    def test_process_log_file(self, mock_file):
        """Tests if LogParser reads and processes a log file correctly."""
        log_file = "fake_path.log"
        self.parser.process_log_file(log_file)

        # Check if counts are correct
        self.assertEqual(self.parser.log_counts[LogType.INFO], 1)
        self.assertEqual(self.parser.log_counts[LogType.ERROR], 1)
        self.assertEqual(self.parser.log_counts[LogType.WARNING], 1)

        # Check if agent responses and errors were captured correctly
        self.assertEqual(self.parser.agent_responses["Hello!"], 1)
        self.assertEqual(self.parser.error_messages["Model Timeout"], 1)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_process_log_file_not_found(self, mock_open):
        """Tests handling when the log file is missing."""
        log_file = "non_existent.log"
        self.parser.process_log_file(log_file)

        # Log counts should be empty since the file doesn't exist
        self.assertEqual(len(self.parser.log_counts), 0)
        self.assertEqual(len(self.parser.agent_responses), 0)
        self.assertEqual(len(self.parser.error_messages), 0)


if __name__ == "__main__":
    unittest.main()
