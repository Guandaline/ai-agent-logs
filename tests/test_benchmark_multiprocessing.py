import os
import pytest
from distributed.multiprocessing_analyzer import process_logs_distributed


@pytest.mark.benchmark
def test_multiprocessing_benchmark(benchmark):
    """Benchmark multiprocessing log analysis with a large log file."""
    log_file = "data/sample_logs.txt"
    assert os.path.exists(log_file), "Log file does not exist"

    # Benchmark the multiprocessing function
    benchmark(process_logs_distributed, log_file, num_workers=4)
