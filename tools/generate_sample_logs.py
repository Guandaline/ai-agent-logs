import random
from datetime import datetime, timedelta
from ai_agent_logs.log_types import LogType

# Definitions
responses = [
    "Hello! How can I help you today?",
    "I'm sorry, I didn't understand that.",
    "Please provide more details.",
    "Let me check that for you.",
    "How can I assist you further?",
]
errors = [
    "Model Timeout after 5000ms",
    "API Connection Failure",
    "Database Query Failed",
    "Invalid User Input",
    "Rate Limit Exceeded",
]
warnings = [
    "High CPU usage detected",
    "Low memory detected",
    "Slow response time detected",
]


def generate_logs(filename: str = "data/sample_logs.txt", num_entries: int = 10000):
    """Generates a synthetic log file."""
    start_time = datetime(2025, 2, 20, 14, 30, 0)

    with open(filename, "w", encoding="utf-8") as log_file:
        for i in range(num_entries):
            timestamp = start_time + timedelta(seconds=i * random.randint(1, 10))
            log_type = random.choice(list(LogType)).value

            if log_type == LogType.INFO.value:
                log_file.write(
                    f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] INFO - Agent Response: \"{random.choice(responses)}\"\n"
                )
            elif log_type == LogType.ERROR.value:
                log_file.write(
                    f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] ERROR - {random.choice(errors)}\n"
                )
            elif log_type == LogType.WARNING.value:
                log_file.write(
                    f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] WARNING - {random.choice(warnings)}\n"
                )

    print(f"Log file generated: {filename}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generates a synthetic log file for testing."
    )
    parser.add_argument(
        "filename",
        type=str,
        nargs="?",
        default="data/large_sample_logs.txt",
        help="Input file name (default: data/sample_logs.txt).",
    )
    parser.add_argument(
        "num_entries",
        type=int,
        nargs="?",
        default=10000,
        help="Number of log entries (default: 10000).",
    )
    args = parser.parse_args()

    generate_logs(args.filename, num_entries=args.num_entries)
