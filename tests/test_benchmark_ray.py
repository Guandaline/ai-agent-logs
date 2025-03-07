import pytest
from distributed.multiprocessing_analyzer import process_logs_distributed


@pytest.mark.benchmark
def test_multiprocessing_performance(benchmark):
    log_file = "data/sample_logs.txt"
    num_workers = 4  # Garante que usamos o número correto de workers
    benchmark(process_logs_distributed, log_file, num_workers)
