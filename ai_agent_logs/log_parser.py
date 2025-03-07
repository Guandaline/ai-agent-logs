import logging
import re
from collections import Counter

from ai_agent_logs.log_types import LogType

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        try:
            line = line.strip()

            if LogType.INFO.value in line:
                self.log_counts[LogType.INFO] += 1
                match = self.RESPONSE_PATTERN.search(line)
                response = match.group(1) if match else None
                if response:
                    self.agent_responses[response] += 1

            elif LogType.ERROR.value in line:
                self.log_counts[LogType.ERROR] += 1
                match = self.ERROR_PATTERN.search(line)
                error_message = match.group(1) if match else "Unknown error"
                self.error_messages[error_message] += 1

            elif LogType.WARNING.value in line:
                self.log_counts[LogType.WARNING] += 1

            else:
                logging.debug(f"Unrecognized log format: {line}")
                return None  # Ignore unrecognized log lines

            logging.debug(f"Processed log line: {line}")
            return True  # Indicates successful processing

        except Exception as e:
            logging.error(f"Error processing log line: {e}")
            return False

    def process_log_file(self, log_file):
        """Reads and processes a log file line by line."""
        try:
            with open(log_file, "r", encoding="utf-8") as file:
                for line in file:
                    self.parse_line(line)

            logging.info(f"Successfully processed log file: {log_file}")

        except FileNotFoundError:
            logging.error(f"Log file not found: {log_file}")
        except Exception as e:
            logging.error(f"Error reading log file {log_file}: {e}")
