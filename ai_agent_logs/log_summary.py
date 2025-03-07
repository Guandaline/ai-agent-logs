import json
import logging
import os
from collections import Counter

from ai_agent_logs.log_parser import LogParser


class LogSummary:
    """Handles the summarization and output of log analysis results."""

    def __init__(self, parser: LogParser):
        self.parser = parser
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def display_results(self):
        """Prints a summary of log analysis."""
        try:
            self.logger.info("Log Summary:")

            for log_type, count in self.parser.log_counts.items():
                self.logger.info(f"- {log_type.name} messages: {count}")

            self.logger.info("\nTop 3 AI Responses:")
            top_responses = Counter(self.parser.agent_responses).most_common(3)
            for response, count in top_responses:
                self.logger.info(f'- "{response}": {count}')

        except Exception as e:
            self.logger.error(f"Error displaying results: {e}")

    def save_results(self, output_file):
        """Saves log analysis results to a JSON file."""
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "log_summary": {
                            k.name: v for k, v in self.parser.log_counts.items()
                        },
                        "common_errors": dict(
                            Counter(self.parser.error_messages).most_common(3)
                        ),
                        "top_responses": dict(
                            Counter(self.parser.agent_responses).most_common(3)
                        ),
                    },
                    f,
                    indent=4,
                )

            self.logger.info(f"Log summary saved successfully to {output_file}")

        except Exception as e:
            self.logger.error(f"Error saving results: {e}")
