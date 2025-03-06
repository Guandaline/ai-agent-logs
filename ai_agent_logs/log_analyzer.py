import logging
import json
import re
import os
from collections import Counter
from ai_agent_logs.log_types import LogType

# Ensure the logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),  # Saves logs to a file
    level=logging.INFO,  # Sets the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class LogAnalyzer:
    def __init__(self, log_file_path):
        """Initializes the LogAnalyzer with the specified log file path."""
        self.log_file_path = log_file_path
        self.log_counts = Counter()
        self.agent_responses = Counter()
        self.error_messages = Counter()
        self.response_pattern = re.compile(r"INFO - Agent Response: \"(.*?)\"")
        self.error_pattern = re.compile(r"ERROR - (.+)")
        logging.info("LogAnalyzer initialized.")

    def parse_log_line(self, line):
        """Processes a single log line."""
        try:
            if LogType.INFO.value in line:
                self.log_counts[LogType.INFO] += 1
                response_match = self.response_pattern.search(line)
                if response_match:
                    self.agent_responses[response_match.group(1)] += 1
            elif LogType.ERROR.value in line:
                self.log_counts[LogType.ERROR] += 1
                error_match = self.error_pattern.search(line)
                if error_match:
                    self.error_messages[error_match.group(1)] += 1
            elif LogType.WARNING.value in line:
                self.log_counts[LogType.WARNING] += 1

            logging.debug(f"Processed log line: {line.strip()}")
        except Exception as e:
            logging.error(f"Error processing log line: {line.strip()} - {e}")

    def parse_log_file(self):
        """Reads the log file and processes each line."""
        logging.info(f"Parsing log file: {self.log_file_path}")
        try:
            with open(self.log_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    self.parse_log_line(line)
            logging.info("Finished parsing log file.")
        except FileNotFoundError:
            logging.error(f"Log file not found: {self.log_file_path}")
        except Exception as e:
            logging.error(f"Error reading log file: {self.log_file_path} - {e}")

    def save_results(self, output_file="data/log_analysis.json"):
        """Saves the analysis results to a JSON file."""
        try:
            results = {
                "log_summary": {
                    log_type.value: count for log_type, count in self.log_counts.items()
                },
                "top_responses": self.agent_responses.most_common(3),
                "common_errors": self.error_messages.most_common(3),
            }

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)
            logging.info(f"Results saved to {output_file}")
        except Exception as e:
            logging.error(f"Error saving results to {output_file}: {e}")

    def display_results(self):
        """Displays the summary of the log analysis."""
        try:
            print("Log Summary:")
            for log_type, count in self.log_counts.items():
                print(f"- {log_type.value} messages: {count}")

            print("\nTop 3 AI Responses:")
            for response, count in self.agent_responses.most_common(3):
                print(f'{count} times - "{response}"')

            print("\nMost Common Errors:")
            for error, count in self.error_messages.most_common(3):
                print(f"{count} times - {error}")
        except Exception as e:
            logging.error(f"Error displaying results: {e}")

    def run(self, save_to_file=True):
        """Executes the entire log analysis pipeline."""
        try:
            self.parse_log_file()
            self.display_results()
            if save_to_file:
                self.save_results()
        except Exception as e:
            logging.critical(f"Unexpected error during execution: {e}")
