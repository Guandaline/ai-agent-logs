import os
import json
import pytest
from io import StringIO
from collections import Counter
from ai_agent_logs.log_analyzer import LogAnalyzer
from ai_agent_logs.log_types import LogType


@pytest.fixture
def log_analyzer():
    """Fixture to create a LogAnalyzer instance."""
    return LogAnalyzer("data/sample_logs.txt")


def test_parse_log_file():
    """Test if log file parsing correctly counts log types, agent responses, and errors."""
    sample_logs = """[2025-02-20 14:32:10] INFO - Agent Response: \"Hello! How can I help you today?\"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: \"I'm sorry, I didn't understand that.\"
[2025-02-20 14:35:10] WARNING - Low memory detected
[2025-02-20 14:36:10] ERROR - API Connection Failure
[2025-02-20 14:37:15] INFO - Agent Response: \"Hello! How can I help you today?\"
[2025-02-20 14:38:10] WARNING - High CPU usage
[2025-02-20 14:39:20] ERROR - Database Query Failed
[2025-02-20 14:40:30] INFO - Agent Response: \"How can I assist you further?\"
"""
    log_analyzer = LogAnalyzer(None)
    log_file_mock = StringIO(sample_logs)
    for line in log_file_mock:
        log_analyzer.parse_log_line(line)

    assert log_analyzer.log_counts == Counter(
        {LogType.INFO: 4, LogType.ERROR: 3, LogType.WARNING: 2}
    )
    assert log_analyzer.agent_responses["Hello! How can I help you today?"] == 2
    assert log_analyzer.agent_responses["I'm sorry, I didn't understand that."] == 1
    assert log_analyzer.agent_responses["How can I assist you further?"] == 1
    assert log_analyzer.error_messages["Model Timeout after 5000ms"] == 1
    assert log_analyzer.error_messages["API Connection Failure"] == 1
    assert log_analyzer.error_messages["Database Query Failed"] == 1


def test_empty_log_file():
    """Test behavior when log file is empty."""
    log_analyzer = LogAnalyzer(None)
    log_file_mock = StringIO("")
    for line in log_file_mock:
        log_analyzer.parse_log_line(line)

    assert log_analyzer.log_counts == Counter()
    assert log_analyzer.agent_responses == Counter()
    assert log_analyzer.error_messages == Counter()


def test_large_log_file():
    """Test parsing a large log file."""
    log_analyzer = LogAnalyzer(None)
    large_logs = "\n".join(
        [f'[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"' for _ in range(10000)]
    )
    log_file_mock = StringIO(large_logs)
    for line in log_file_mock:
        log_analyzer.parse_log_line(line)

    assert log_analyzer.log_counts[LogType.INFO] == 10000
    assert log_analyzer.agent_responses["Hello!"] == 10000
    assert log_analyzer.log_counts[LogType.ERROR] == 0
    assert log_analyzer.log_counts[LogType.WARNING] == 0


def test_display_results(log_analyzer, capsys):
    """Test if display_results prints the expected output."""
    log_analyzer.log_counts = Counter(
        {LogType.INFO: 3, LogType.ERROR: 2, LogType.WARNING: 1}
    )
    log_analyzer.agent_responses = Counter(
        {"Hello!": 2, "I'm sorry, I didn't understand that.": 1}
    )
    log_analyzer.error_messages = Counter({"API Connection Failure": 2})

    log_analyzer.display_results()

    captured = capsys.readouterr()
    assert "Log Summary:" in captured.out
    assert "INFO messages: 3" in captured.out
    assert "ERROR messages: 2" in captured.out
    assert "Most Common Errors:" in captured.out
    assert "API Connection Failure" in captured.out


def test_parse_nonexistent_file(caplog):
    """Test if LogAnalyzer logs an error when a file does not exist."""
    log_analyzer = LogAnalyzer("data/nonexistent_file.txt")

    log_analyzer.parse_log_file()

    assert any("Log file not found" in record.message for record in caplog.records)


def test_save_results(log_analyzer):
    """Test if results are saved correctly to a JSON file."""
    log_analyzer.log_counts = Counter(
        {LogType.INFO: 5, LogType.ERROR: 2, LogType.WARNING: 1}
    )
    log_analyzer.agent_responses = Counter(
        {"Hello!": 3, "Please provide more details.": 2}
    )
    log_analyzer.error_messages = Counter({"Model Timeout after 5000ms": 2})

    output_file = "data/test_log_analysis.json"
    log_analyzer.save_results(output_file)

    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["log_summary"]["INFO"] == 5
    assert data["log_summary"]["ERROR"] == 2
    assert data["common_errors"][0][1] == 2

    os.remove(output_file)  # Cleanup
