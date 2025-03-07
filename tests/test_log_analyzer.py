import unittest
from unittest.mock import patch, mock_open
from collections import Counter
from ai_agent_logs.log_analyzer import LogAnalyzer


class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up a fresh LogAnalyzer instance for each test."""
        self.analyzer = LogAnalyzer()

    def test_parse_log_line(self):
        """Test if a single log line is correctly parsed."""
        sample_log_entry = '[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"\n'
        self.analyzer.parse_log_line(sample_log_entry)

        self.assertEqual(self.analyzer.log_counts["INFO"], 1)
        self.assertEqual(self.analyzer.agent_responses["Hello!"], 1)

    def test_multiple_log_entries(self):
        """Test processing multiple log lines."""
        sample_logs = """[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] WARNING - Low memory detected
[2025-02-20 14:35:10] INFO - Agent Response: "I'm sorry, I didn't understand that."
"""
        for line in sample_logs.split("\n"):
            if line.strip():
                self.analyzer.parse_log_line(line)

        self.assertEqual(
            self.analyzer.log_counts, Counter({"INFO": 2, "ERROR": 1, "WARNING": 1})
        )
        self.assertEqual(self.analyzer.agent_responses["Hello!"], 1)
        self.assertEqual(
            self.analyzer.agent_responses["I'm sorry, I didn't understand that."], 1
        )
        self.assertEqual(self.analyzer.error_messages["Model Timeout after 5000ms"], 1)

    def test_save_results(self):
        """Test saving results to a JSON file."""
        self.analyzer.log_counts = Counter({"INFO": 3, "ERROR": 2, "WARNING": 1})
        self.analyzer.agent_responses = Counter(
            {"Hello!": 2, "I'm sorry, I didn't understand that.": 1}
        )
        self.analyzer.error_messages = Counter({"Model Timeout after 5000ms": 2})

        with patch("builtins.open", mock_open()) as mock_file:
            self.analyzer.save_results("fake_output.json")
            mock_file.assert_called_once_with("fake_output.json", "w", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
