import json
import os
import ray
from collections import Counter


class LogAnalyzer:
    def __init__(self):
        self.log_counts = Counter()
        self.agent_responses = Counter()
        self.error_messages = Counter()

    def parse_log_line(self, line):
        """Parses a single log line and updates the counters."""
        if "INFO" in line:
            self.log_counts["INFO"] += 1
        elif "ERROR" in line:
            self.log_counts["ERROR"] += 1
        elif "WARNING" in line:
            self.log_counts["WARNING"] += 1

        if "Agent Response:" in line:
            response = line.split("Agent Response:")[1].strip().strip('"')
            self.agent_responses[response] += 1
        elif "ERROR -" in line:
            error_msg = line.split("ERROR - ")[1].strip()
            self.error_messages[error_msg] += 1


    def save_results(self, output_file):
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "log_summary": dict(self.log_counts),
                        "common_errors": self.error_messages.most_common(3),
                    },
                    f,
                    indent=4,
                )
        except Exception as e:
            print(f"Error saving results: {e}")


@ray.remote
def process_log_chunk(lines):
    """Processes a chunk of log lines."""
    log_analyzer = LogAnalyzer()
    for line in lines:
        log_analyzer.parse_log_line(line)
    return log_analyzer.log_counts


def process_logs_ray(log_file, num_workers=4):
    """Processes logs using Ray for distributed execution."""
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

    print("\n⚡ Ray Distributed Log Analysis Completed!")
    for log_type, count in final_counts.items():
        print(f"{log_type}: {count}")


if __name__ == "__main__":
    log_file = "data/sample_logs.txt"
    process_logs_ray(log_file)
