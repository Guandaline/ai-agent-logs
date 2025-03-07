import re
import logging
from collections import Counter
from ai_agent_logs.log_types import LogType


class LogParser:
    """Handles the extraction of information from log files."""

    RESPONSE_PATTERN = re.compile(r'INFO - Agent Response: "(.*?)"')
    ERROR_PATTERN = re.compile(r"ERROR - (.+)")

    def __init__(self):
        self.log_counts = Counter()
        self.agent_responses = Counter()
        self.error_messages = Counter()

    def parse_line(self, line):
        """Parses a single log line and updates counters."""
        if LogType.INFO.value in line:
            self.log_counts[LogType.INFO] += 1
            match = self.RESPONSE_PATTERN.search(line)
            if match:
                self.agent_responses[match.group(1)] += 1

        elif LogType.ERROR.value in line:
            self.log_counts[LogType.ERROR] += 1
            match = self.ERROR_PATTERN.search(line)
            if match:
                self.error_messages[match.group(1)] += 1

        elif LogType.WARNING.value in line:
            self.log_counts[LogType.WARNING] += 1

        logging.debug(f"Processed log line: {line.strip()}")
