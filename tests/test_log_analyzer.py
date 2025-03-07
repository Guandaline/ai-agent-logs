import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from ai_agent_logs.log_analyzer import LogAnalyzer
from ai_agent_logs.log_parser import LogParser
from ai_agent_logs.log_summary import LogSummary


class TestLogAnalyzer(unittest.TestCase):
    """Test suite for LogAnalyzer."""

    def setUp(self):
        """Setup temporary log file and mock dependencies."""
        self.temp_log = tempfile.NamedTemporaryFile(
            delete=False, mode="w", encoding="utf-8"
        )
        self.temp_log.write('[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"\n')
        self.temp_log.write("[2025-02-20 14:32:15] ERROR - Model Timeout\n")
        self.temp_log.write("[2025-02-20 14:32:20] WARNING - High Latency\n")
        self.temp_log.close()  # Close to allow reading

        self.output_file = "output/test_log_summary.json"

    def tearDown(self):
        """Cleanup temporary files."""
        os.remove(self.temp_log.name)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_run_process_logs(self):
        """Test if run() processes the logs correctly and returns summary and parser."""
        analyzer = LogAnalyzer(self.temp_log.name, self.output_file)
        log_summary, log_parser = analyzer.run()

        self.assertIsInstance(log_summary, LogSummary)
        self.assertIsInstance(log_parser, LogParser)
        self.assertGreaterEqual(len(log_parser.log_counts), 1)

    def test_run_file_not_found(self):
        """Test handling of missing log file."""
        analyzer = LogAnalyzer("non_existent_file.log", self.output_file)

        with self.assertLogs(level="ERROR") as log:
            result = analyzer.run()

        self.assertIsNone(result)
        self.assertIn("Log file not found", log.output[0])

    def test_run_creates_output_file(self):
        """Test that run() generates the expected output file."""
        analyzer = LogAnalyzer(self.temp_log.name, self.output_file)
        analyzer.run()
        self.assertTrue(os.path.exists(self.output_file))


if __name__ == "__main__":
    unittest.main()
