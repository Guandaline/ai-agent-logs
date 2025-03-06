import argparse
from ai_agent_logs.log_analyzer import LogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="AI Agent Log Analyzer")
    parser.add_argument(
        "log_file",
        nargs="?",
        default="data/sample_logs.txt",
        help="Path to the log file",
    )
    parser.add_argument(
        "--no-save",
        action="store_false",
        dest="save_to_file",
        help="Disable saving results to a JSON file",
    )
    args = parser.parse_args()

    analyzer = LogAnalyzer(args.log_file)
    analyzer.run(save_to_file=args.save_to_file)


if __name__ == "__main__":
    main()
