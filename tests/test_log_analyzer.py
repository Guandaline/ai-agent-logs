import unittest
from io import StringIO
from collections import Counter
from ai_agent_logs.log_analyzer import LogAnalyzer
from ai_agent_logs.log_types import LogType

class TestLogAnalyzerExtended(unittest.TestCase):
    def setUp(self):
        self.sample_logs = """[2025-02-20 14:32:10] INFO - Agent Response: \"Hello! How can I help you today?\"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: \"I'm sorry, I didn't understand that.\"
[2025-02-20 14:35:10] WARNING - Low memory detected
[2025-02-20 14:36:10] ERROR - API Connection Failure
[2025-02-20 14:37:15] INFO - Agent Response: \"Hello! How can I help you today?\"
[2025-02-20 14:38:10] WARNING - High CPU usage
[2025-02-20 14:39:20] ERROR - Database Query Failed
[2025-02-20 14:40:30] INFO - Agent Response: \"How can I assist you further?\"
"""

    def test_parse_log_file(self):
        log_analyzer = LogAnalyzer(None)
        log_analyzer.log_counts = Counter()
        log_analyzer.agent_responses = Counter()
        log_analyzer.error_messages = Counter()

        log_file_mock = StringIO(self.sample_logs)
        for line in log_file_mock:
            log_analyzer.parse_log_line(line)

        # Verifica a contagem das mensagens
        self.assertEqual(
            log_analyzer.log_counts,
            Counter({LogType.INFO: 4, LogType.ERROR: 3, LogType.WARNING: 2}),
        )

        # Verifica as respostas do agente
        self.assertEqual(
            log_analyzer.agent_responses["Hello! How can I help you today?"], 2
        )
        self.assertEqual(
            log_analyzer.agent_responses["I'm sorry, I didn't understand that."], 1
        )
        self.assertEqual(
            log_analyzer.agent_responses["How can I assist you further?"], 1
        )

        # Verifica os erros mais comuns
        self.assertEqual(log_analyzer.error_messages["Model Timeout after 5000ms"], 1)
        self.assertEqual(log_analyzer.error_messages["API Connection Failure"], 1)
        self.assertEqual(log_analyzer.error_messages["Database Query Failed"], 1)

    def test_empty_log_file(self):
        log_analyzer = LogAnalyzer(None)
        log_analyzer.log_counts = Counter()
        log_analyzer.agent_responses = Counter()
        log_analyzer.error_messages = Counter()

        log_file_mock = StringIO("")
        for line in log_file_mock:
            log_analyzer.parse_log_line(line)

        self.assertEqual(log_analyzer.log_counts, Counter())
        self.assertEqual(log_analyzer.agent_responses, Counter())
        self.assertEqual(log_analyzer.error_messages, Counter())

    def test_large_log_file(self):
        log_analyzer = LogAnalyzer(None)
        log_analyzer.log_counts = Counter()
        log_analyzer.agent_responses = Counter()
        log_analyzer.error_messages = Counter()

        large_logs = "\n".join(
            [
                f'[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"'
                for _ in range(10000)
            ]
        )
        log_file_mock = StringIO(large_logs)
        for line in log_file_mock:
            log_analyzer.parse_log_line(line)

        self.assertEqual(log_analyzer.log_counts[LogType.INFO], 10000)
        self.assertEqual(log_analyzer.agent_responses["Hello!"], 10000)
        self.assertEqual(log_analyzer.log_counts[LogType.ERROR], 0)
        self.assertEqual(log_analyzer.log_counts[LogType.WARNING], 0)


if __name__ == "__main__":
    unittest.main()
