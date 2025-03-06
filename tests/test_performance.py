import pytest
from ai_agent_logs.log_analyzer import LogAnalyzer
from io import StringIO


@pytest.mark.benchmark
def test_large_log_performance(benchmark):
    """Testa o tempo de execução do parser em um log grande"""
    large_logs = "\n".join(
        [
            f'[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"'
            for _ in range(500000)
        ]
    )
    log_file_mock = StringIO(large_logs)
    analyzer = LogAnalyzer(None)

    # Benchmark para medir tempo de execução
    benchmark(lambda: [analyzer.parse_log_line(line) for line in log_file_mock])
