import json
import os
import ray
from collections import Counter
from ai_agent_logs.log_analyzer import (
    LogAnalyzer,
)  # Importing the LogAnalyzer from the main module


@ray.remote
def process_log_chunk(lines):
    """Processes a chunk of log lines using LogAnalyzer."""
    log_analyzer = LogAnalyzer()
    for line in lines:
        log_analyzer.parse_log_line(line)
    return {
        "log_counts": dict(log_analyzer.log_counts),
        "agent_responses": dict(log_analyzer.agent_responses),
        "error_messages": dict(log_analyzer.error_messages),
    }


def process_logs_ray(log_file, num_workers=4):
    """Processes logs using Ray for distributed execution."""
    if not os.path.exists(log_file):
        print(f"Error: Log file '{log_file}' not found.")
        return

    with open(log_file, "r", encoding="utf-8") as f:
        log_lines = f.readlines()

    if not log_lines:
        print("Warning: The log file is empty.")
        return

    chunk_size = len(log_lines) // num_workers or 1
    log_chunks = [
        log_lines[i : i + chunk_size] for i in range(0, len(log_lines), chunk_size)
    ]

    ray.init(ignore_reinit_error=True)
    futures = [process_log_chunk.remote(chunk) for chunk in log_chunks]
    results = ray.get(futures)

    # Aggregate results
    final_counts = Counter()
    final_responses = Counter()
    final_errors = Counter()

    for result in results:
        final_counts.update(result["log_counts"])
        final_responses.update(result["agent_responses"])
        final_errors.update(result["error_messages"])

    # Display results
    print("\n⚡ Ray Distributed Log Analysis Completed!")
    print(f"INFO: {final_counts.get('INFO', 0)}")
    print(f"ERROR: {final_counts.get('ERROR', 0)}")
    print(f"WARNING: {final_counts.get('WARNING', 0)}")

    print("\nTop 3 AI Responses:")
    for response, count in final_responses.most_common(3):
        print(f'{count} times - "{response}"')

    print("\nMost Common Errors:")
    for error, count in final_errors.most_common(3):
        print(f"{count} times - {error}")

    # Save results
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
        print(f"\n📂 Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    log_file = "data/sample_logs.txt"
    num_workers = 4  # Adjust the number of workers if needed
    process_logs_ray(log_file, num_workers)
