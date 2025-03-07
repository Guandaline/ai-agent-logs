import os
import pytest
import ray
from distributed.ray_analyzer import process_logs_ray


@pytest.mark.slow
def test_ray_analysis(capfd):
    """Test Ray distributed log processing and validate log counts."""
    log_file = "data/sample_logs.txt"
    assert os.path.exists(log_file), "Log file does not exist"

    # Start Ray if not already running
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)

    # Capture output
    process_logs_ray(log_file, num_workers=2)
    captured = capfd.readouterr()

    # Validate output structure
    assert "Ray Distributed Log Analysis Completed!" in captured.out
    assert "INFO:" in captured.out
    assert "ERROR:" in captured.out
    assert "WARNING:" in captured.out
    assert "Top 3 AI Responses:" in captured.out
    assert "Most Common Errors:" in captured.out

    # Extract counts from output
    lines = captured.out.split("\n")
    log_counts = {}

    for line in lines:
        if "INFO:" in line or "ERROR:" in line or "WARNING:" in line:
            key, value = line.split(":")
            log_counts[key.strip()] = int(value.strip())

    # Ensure logs are being counted properly
    assert log_counts["INFO"] > 0, "INFO count is incorrect"
    assert log_counts["ERROR"] > 0, "ERROR count is incorrect"
    assert log_counts["WARNING"] > 0, "WARNING count is incorrect"


if __name__ == "__main__":
    pytest.main(["-v", "tests/test_ray.py"])
