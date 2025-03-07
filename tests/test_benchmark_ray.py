import os
import pytest
import ray
from distributed.ray_analyzer import process_logs_ray


@pytest.mark.benchmark
def test_ray_benchmark(benchmark):
    """Benchmark Ray distributed log processing with a large log file."""
    log_file = "data/sample_logs.txt"
    assert os.path.exists(log_file), "Log file does not exist"

    # Start Ray if not already running
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)

    # Benchmark the Ray function
    benchmark(process_logs_ray, log_file, num_workers=4)
