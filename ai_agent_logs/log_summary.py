import json
import os
from collections import Counter
import logging


class LogSummary:
    
    """Handles the summarization and output of log analysis results."""

    def __init__(self, parser):
        self.parser = parser  # Recebe um LogParser para gerar os resumos
        self.agent_responses = Counter()

    def display_results(self):
        """Prints a summary of log analysis."""
        logger = logging.getLogger()
        logger.info("Log Summary:")
        
        for log_type, count in self.parser.log_counts.items():
            logger.info(f"- {log_type} messages: {count}")  # 🔹 Use logger instead of print
        
        logger.info("\nTop 3 AI Responses:")
        top_responses = Counter(self.parser.agent_responses).most_common(3)  # 🔹 Convert to Counter
        for response, count in top_responses:
            logger.info(f'- "{response}": {count}')

    def save_results(self, output_file):
        """Saves log analysis results to a JSON file."""
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({
                    "log_summary": {k.name: v for k, v in self.parser.log_counts.items()},  # 🔹 Use .name to obtain "INFO", "ERROR", etc.
                    "common_errors": dict(Counter(self.parser.error_messages).most_common(3)),
                    "top_responses": dict(Counter(self.parser.agent_responses).most_common(3))
                }, f, indent=4)
        except Exception as e:
            print(f"Error saving results: {e}")
