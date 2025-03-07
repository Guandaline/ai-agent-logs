import ray
from collections import Counter
from ai_agent_logs.log_analyzer import LogAnalyzer
from ai_agent_logs.log_types import LogType

# Initialize Ray
ray.init(ignore_reinit_error=True)


@ray.remote
def process_log_chunk(log_chunk):
    """Processes a chunk of log lines in a Ray worker and returns counts."""
    log_analyzer = LogAnalyzer(None)

    log_counts = Counter({LogType.INFO: 0, LogType.ERROR: 0, LogType.WARNING: 0})
    agent_responses = Counter()
    error_messages = Counter()

    # Process each line
    for line in log_chunk:
        log_analyzer.parse_log_line(line)

    # Assign parsed counts to local counters (no cumulative updates inside loop)
    log_counts.update(log_analyzer.log_counts)
    agent_responses.update(log_analyzer.agent_responses)
    error_messages.update(log_analyzer.error_messages)

    return (
        dict(log_counts),
        dict(agent_responses),
        dict(error_messages),
    )  # Convert to dicts for serialization


def process_logs_ray(log_file_path, num_workers=4):
    """Executes distributed log analysis using Ray."""
    with open(log_file_path, "r", encoding="utf-8") as f:
        log_lines = f.readlines()

    # Ensure at least one worker and avoid zero chunk size
    num_workers = min(num_workers, len(log_lines)) or 1
    chunk_size = max(1, len(log_lines) // num_workers)

    # Distribute logs into equal chunks without overlap
    log_chunks = [
        log_lines[i : i + chunk_size] for i in range(0, len(log_lines), chunk_size)
    ]

    # Dispatch tasks to Ray workers
    futures = [process_log_chunk.remote(chunk) for chunk in log_chunks]
    results = ray.get(futures)  # Retrieve results from workers

    # Initialize counters
    final_counts = Counter({LogType.INFO: 0, LogType.ERROR: 0, LogType.WARNING: 0})
    final_responses = Counter()
    final_errors = Counter()

    # Aggregate results from workers
    for log_counts, agent_responses, error_messages in results:
        final_counts.update(log_counts)
        final_responses.update(agent_responses)
        final_errors.update(error_messages)

    # Convert Enum keys to strings for proper display
    final_counts = {key.value: value for key, value in final_counts.items()}

    print("\n⚡ Ray Distributed Log Analysis Completed!")
    print("INFO:", final_counts.get("INFO", 0))
    print("ERROR:", final_counts.get("ERROR", 0))
    print("WARNING:", final_counts.get("WARNING", 0))
    print("Top 3 AI Responses:", final_responses.most_common(3))
    print("Most Common Errors:", final_errors.most_common(3))


if __name__ == "__main__":
    log_file = "data/sample_logs.txt"
    num_workers = 4  # Number of workers
    process_logs_ray(log_file, num_workers)
