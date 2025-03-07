import os

from tools.generate_sample_logs import generate_logs


def test_generate_logs():
    """Test if the synthetic log generator creates a file with expected content."""
    test_file = "data/test_generated_logs.txt"
    generate_logs(test_file, num_entries=50)

    assert os.path.exists(test_file)

    with open(test_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 50  # Verify expected number of lines

    os.remove(test_file)  # Cleanup
