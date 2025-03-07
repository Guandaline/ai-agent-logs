import pytest

from distributed.ray_analyzer import process_logs_ray


@pytest.mark.benchmark
def test_ray_performance(benchmark):
    """Benchmark Ray's performance for log processing."""
    log_file = "data/sample_logs.txt"

    benchmark(lambda: process_logs_ray(log_file, num_workers=2))
