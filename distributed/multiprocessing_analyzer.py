import logging
import os
from collections import Counter
from multiprocessing import Pool, get_logger

from ai_agent_logs.log_parser import LogParser

# Configure multiprocessing logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def setup_logger():
    """Ensures that multiprocessing workers log messages properly."""
    logger = get_logger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


def process_log_chunk(lines):
    """Processes a chunk of log lines."""
    logger = get_logger()
    logger.info(f"Processing chunk with {len(lines)} lines.")

    parser = LogParser()
    for line in lines:
        parser.parse_line(line)

    return {
        "log_counts": parser.log_counts,
        "agent_responses": parser.agent_responses,
        "error_messages": parser.error_messages,
    }


def process_logs_distributed(log_file, num_workers=4):
    """Processes logs using multiprocessing."""
    if not os.path.exists(log_file):
        logging.error(f"Log file not found: {log_file}")
        return None

    logging.info(f"Starting multiprocessing log processing with {num_workers} workers.")

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            log_lines = f.readlines()

        chunk_size = len(log_lines) // num_workers or 1
        log_chunks = [
            log_lines[i: i + chunk_size] for i in range(0, len(log_lines), chunk_size)
        ]

        logging.info(f"Log file split into {len(log_chunks)} chunks.")

        with Pool(processes=num_workers, initializer=setup_logger) as pool:
            results = pool.map(process_log_chunk, log_chunks)

        # Merge results from workers
        final_counts = Counter()
        final_responses = Counter()
        final_errors = Counter()

        for result in results:
            final_counts.update(result["log_counts"])
            final_responses.update(result["agent_responses"])
            final_errors.update(result["error_messages"])

        # Log final results
        print(
            "\n⚡ Multiprocessing Log Analysis Completed!"
        )  # <-- Garantindo saída visível no pytest
        for log_type, count in final_counts.items():
            print(f"{log_type.name}: {count}")

        print("\nTop 3 AI Responses:")
        for response, count in final_responses.most_common(3):
            print(f'- "{response}": {count}')

        print("\nMost Common Errors:")
        for error, count in final_errors.most_common(3):
            print(f"- {error}: {count}")

        return final_counts, final_responses, final_errors

    except Exception as e:
        logging.error(f"An error occurred during log processing: {e}")
        return None


if __name__ == "__main__":
    log_file = "data/sample_logs.txt"
    num_workers = 4  # Adjust the number of workers if needed
    process_logs_distributed(log_file, num_workers)
