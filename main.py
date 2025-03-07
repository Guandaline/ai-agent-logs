import argparse
import logging

from ai_agent_logs.log_analyzer import LogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Log Analyzer CLI")
    parser.add_argument(
        "log_file",
        nargs="?",
        default="data/sample_logs.txt",
        help="Path to the log file (optional)",
    )
    parser.add_argument(
        "--output",
        nargs="?",
        default="data/log_summary.json",
        help="Path to save the log summary (optional)",
    )
    args = parser.parse_args()

    # Run the analyzer with the provided arguments
    analyzer = LogAnalyzer(args.log_file, args.output)
    log_summary = analyzer.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
