import unittest
from ai_agent_logs.log_parser import LogParser
from ai_agent_logs.log_types import LogType


class TestLogParser(unittest.TestCase):
    def setUp(self):
        """Creates a LogParser instance before each test."""
        self.parser = LogParser()

    def test_parse_info_log(self):
        """Tests parsing INFO logs with agent responses."""
        log_line = '[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"'
        self.parser.parse_line(log_line)
        self.assertEqual(self.parser.log_counts[LogType.INFO], 1)
        self.assertEqual(self.parser.agent_responses["Hello!"], 1)

    def test_parse_error_log(self):
        """Tests parsing ERROR logs."""
        log_line = "[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms"
        self.parser.parse_line(log_line)
        self.assertEqual(self.parser.log_counts[LogType.ERROR], 1)
        self.assertEqual(self.parser.error_messages["Model Timeout after 5000ms"], 1)

    def test_parse_warning_log(self):
        """Tests parsing WARNING logs."""
        log_line = "[2025-02-20 14:35:10] WARNING - High CPU usage"
        self.parser.parse_line(log_line)
        self.assertEqual(self.parser.log_counts[LogType.WARNING], 1)

    def test_empty_log(self):
        """Tests that an empty log doesn't break parsing."""
        self.parser.parse_line("")
        self.assertEqual(sum(self.parser.log_counts.values()), 0)


if __name__ == "__main__":
    unittest.main()
