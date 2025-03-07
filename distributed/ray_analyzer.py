import json
import logging
import os
from collections import Counter

import ray

from ai_agent_logs.log_parser import LogParser

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@ray.remote
def process_log_chunk(lines):
    """
    Processes a chunk of log lines.

    This function is executed in parallel using Ray workers.
    Each worker processes a subset of the log lines and returns the parsed results.
    """
    log_parser = LogParser()

    for line in lines:
        log_parser.parse_line(line)

    return {
        "log_counts": {
            str(k).split(".")[-1]: v for k, v in log_parser.log_counts.items()
        },  # Convert Enum keys to strings
        "agent_responses": dict(log_parser.agent_responses),
        "error_messages": dict(log_parser.error_messages),
    }


def process_logs_ray(log_file, num_workers=4):
    """
    Processes logs using Ray for distributed execution.

    This function reads the log file, splits it into chunks, distributes the processing
    among multiple workers, and aggregates the results.

    Args:
        log_file (str): Path to the log file.
        num_workers (int): Number of Ray workers to use.
    """
    if not os.path.exists(log_file):
        logging.error(f"Log file '{log_file}' not found.")
        return

    with open(log_file, "r", encoding="utf-8") as f:
        log_lines = f.readlines()

    if not log_lines:
        logging.warning("The log file is empty.")
        return

    # Split logs into chunks for parallel processing
    chunk_size = max(1, len(log_lines) // num_workers)
    log_chunks = [
        log_lines[i: i + chunk_size] for i in range(0, len(log_lines), chunk_size)
    ]

    # Initialize Ray
    ray.init(ignore_reinit_error=True)
    logging.info("Ray initialized with %d workers.", num_workers)

    # Dispatch processing tasks to workers
    futures = [process_log_chunk.remote(chunk) for chunk in log_chunks]
    results = ray.get(futures)

    logging.info("\nRaw results from workers: %s", results)

    # Aggregate results
    final_counts = Counter()
    final_responses = Counter()
    final_errors = Counter()

    for result in results:
        logging.debug("\nWorker result: %s", result)  # Log worker results for debugging
        final_counts.update(result["log_counts"])
        final_responses.update(result["agent_responses"])
        final_errors.update(result["error_messages"])

    # Display summarized results
    logging.info("\n⚡ Ray Distributed Log Analysis Completed!")
    logging.info(f"INFO: {final_counts.get('INFO', 0)}")
    logging.info(f"ERROR: {final_counts.get('ERROR', 0)}")
    logging.info(f"WARNING: {final_counts.get('WARNING', 0)}")

    logging.info("\nTop 3 AI Responses:")
    for response, count in final_responses.most_common(3):
        logging.info(f'{count} times - "{response}"')

    logging.info("\nMost Common Errors:")
    for error, count in final_errors.most_common(3):
        logging.info(f"{count} times - {error}")

    # Save results to a JSON file
    output_file = "data/ray_log_analysis.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "log_summary": dict(final_counts),
                    "top_responses": final_responses.most_common(3),
                    "common_errors": final_errors.most_common(3),
                },
                f,
                indent=4,
            )
        logging.info(f"\nResults saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving results: {e}")


if __name__ == "__main__":
    log_file = "data/sample_logs.txt"
    num_workers = 4  # Adjust the number of workers if needed
    process_logs_ray(log_file, num_workers)
