import logging
import os

import pytest
import ray

from distributed.ray_analyzer import process_logs_ray


@pytest.mark.slow
def test_ray_analysis(caplog):
    """Test Ray distributed log processing and validate log counts."""
    log_file = "data/sample_logs.txt"
    assert os.path.exists(log_file), "Log file does not exist"

    # Enable capturing logs
    caplog.set_level(logging.INFO)

    # Start Ray if not already running
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)

    # Run the log analysis
    process_logs_ray(log_file, num_workers=2)

    # 🔹 Debug: Print captured logs for troubleshooting
    print("\nCaptured Logs:\n", caplog.text)

    # Validate log output
    assert "Ray Distributed Log Analysis Completed!" in caplog.text
    assert "INFO:" in caplog.text
    assert "ERROR:" in caplog.text
    assert "WARNING:" in caplog.text
    assert "Top 3 AI Responses:" in caplog.text
    assert "Most Common Errors:" in caplog.text

    # Extract counts from logs
    log_counts = {}
    for record in caplog.records:
        message = record.message
        if any(log_type in message for log_type in ["INFO:", "ERROR:", "WARNING:"]):
            parts = message.rsplit(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                if value.isdigit():
                    log_counts[key] = int(value)

    # Ensure logs are counted correctly
    assert log_counts.get("INFO", 0) > 0, "INFO count is incorrect"
    assert log_counts.get("ERROR", 0) > 0, "ERROR count is incorrect"
    assert log_counts.get("WARNING", 0) > 0, "WARNING count is incorrect"


if __name__ == "__main__":
    pytest.main(["-v", "tests/test_ray.py"])
