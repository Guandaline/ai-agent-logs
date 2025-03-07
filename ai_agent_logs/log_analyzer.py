import logging
import os
from collections import Counter

import ray

from ai_agent_logs.log_parser import LogParser
from ai_agent_logs.log_summary import LogSummary

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class LogAnalyzer:
    """Handles log analysis by orchestrating parsing and summarization."""

    def __init__(self, log_file: str, output_file: str = None):
        self.log_file = log_file
        self.output_file = output_file

    def run(self):
        """Executes the log analysis workflow."""
        try:
            logging.info("Starting log analysis...")

            if not os.path.exists(self.log_file):
                logging.error(f"Log file not found: {self.log_file}")
                return None

            # Create and process the log parser
            log_parser = LogParser()
            log_parser.process_log_file(self.log_file)

            # Create and use LogSummary
            log_summary = LogSummary(log_parser)

            if self.output_file:
                log_summary.save_results(self.output_file)
                logging.info(f"Log summary saved to {self.output_file}")

            return log_summary, log_parser

        except Exception as e:
            logging.error(f"An error occurred: {e}")


@ray.remote
def process_log_chunk(lines):
    """Processes a chunk of log lines in parallel."""
    log_analyzer = LogAnalyzer()
    for line in lines:
        log_analyzer.process_logs(line)
    return log_analyzer.log_counts


def process_logs_ray(log_file, num_workers=4):
    """Processes logs using Ray for distributed execution."""
    if not os.path.exists(log_file):
        logging.error(f"Log file '{log_file}' not found.")
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            log_lines = f.readlines()

        chunk_size = len(log_lines) // num_workers or 1
        log_chunks = [
            log_lines[i : i + chunk_size] for i in range(0, len(log_lines), chunk_size)
        ]

        ray.init(ignore_reinit_error=True)
        futures = [process_log_chunk.remote(chunk) for chunk in log_chunks]
        results = ray.get(futures)

        final_counts = Counter()
        for result in results:
            final_counts.update(result)

        logging.info("\n⚡ Ray Distributed Log Analysis Completed!")
        for log_type, count in final_counts.items():
            logging.info(f"{log_type}: {count}")
    except Exception as e:
        logging.error(f"Error processing logs with Ray: {e}")


if __name__ == "__main__":
    log_file = "data/sample_logs.txt"
    analyzer = LogAnalyzer(log_file)
    analyzer.ru()
