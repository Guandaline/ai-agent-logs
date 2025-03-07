from io import StringIO

import pytest

from ai_agent_logs.log_analyzer import LogAnalyzer


@pytest.mark.benchmark
def test_analyzer_performance(benchmark, tmp_path):
    """Test the performance of LogAnalyzer on a large log file."""

    large_logs = "\n".join(
        [
            f'[2025-02-20 14:32:10] INFO - Agent Response: "Hello!"'
            for _ in range(500000)
        ]
    )

    log_file_path = tmp_path / "large_log.txt"
    log_file_path.write_text(large_logs)

    # ✅ Agora passamos o caminho do arquivo para o LogAnalyzer corretamente
    analyzer = LogAnalyzer(str(log_file_path))

    # Benchmark o tempo de execução do `run()`
    benchmark(analyzer.run)
