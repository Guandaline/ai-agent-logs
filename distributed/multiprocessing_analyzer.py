import multiprocessing
import os
from collections import Counter
from ai_agent_logs.log_analyzer import LogAnalyzer
from ai_agent_logs.log_types import LogType  # ✅ Importing LogType globally


def process_log_chunk(log_chunk):
    """Processes a chunk of log lines and returns the counts."""
    from ai_agent_logs.log_types import (
        LogType,
    )  # ✅ Explicitly import LogType inside the function

    log_analyzer = LogAnalyzer()

    # Ensure we initialize fresh counters for each process
    log_counts = Counter({LogType.INFO: 0, LogType.ERROR: 0, LogType.WARNING: 0})
    agent_responses = Counter()
    error_messages = Counter()

    for line in log_chunk:
        log_analyzer.parse_log_line(line)

        # Manually update local counters
        log_counts.update(log_analyzer.log_counts)
        agent_responses.update(log_analyzer.agent_responses)
        error_messages.update(log_analyzer.error_messages)

    return log_counts, agent_responses, error_messages


def process_logs_distributed(log_file_path, num_workers=4):
    """Executes distributed log analysis using multiprocessing."""
    with open(log_file_path, "r", encoding="utf-8") as f:
        log_lines = f.readlines()

    # Ensure at least one worker and avoid chunk_size = 0
    num_workers = min(num_workers, len(log_lines)) or 1
    chunk_size = max(1, len(log_lines) // num_workers)

    log_chunks = [
        log_lines[i : i + chunk_size] for i in range(0, len(log_lines), chunk_size)
    ]

    # Process log chunks in parallel
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(process_log_chunk, log_chunks)

    # Combine results from all workers
    final_counts = Counter({LogType.INFO: 0, LogType.ERROR: 0, LogType.WARNING: 0})
    final_responses = Counter()
    final_errors = Counter()

    for log_counts, agent_responses, error_messages in results:
        final_counts.update(log_counts)
        final_responses.update(agent_responses)
        final_errors.update(error_messages)

    # Convert Enum keys to strings for proper display
    final_counts = {str(key): value for key, value in final_counts.items()}

    print("\n🚀 Multiprocessing Log Analysis Completed!")
    print("INFO:", final_counts.get("INFO", 0))
    print("ERROR:", final_counts.get("ERROR", 0))
    print("WARNING:", final_counts.get("WARNING", 0))
    print("Top 3 AI Responses:", final_responses.most_common(3))
    print("Most Common Errors:", final_errors.most_common(3))


if __name__ == "__main__":
    log_file = "data/large_sample_logs.txt"
    num_workers = os.cpu_count() or 4  # Use the maximum available CPU cores
    process_logs_distributed(log_file, num_workers)
