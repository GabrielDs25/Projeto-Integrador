from src.evaluation import accuracy_rate, average_response_time


def test_accuracy_rate():
    results = [
        {"correct": True},
        {"correct": False},
        {"correct": True},
    ]
    assert accuracy_rate(results) == 2 / 3


def test_accuracy_rate_empty_list():
    assert accuracy_rate([]) == 0.0


def test_average_response_time():
    results = [{"seconds": 1.0}, {"seconds": 3.0}]
    assert average_response_time(results) == 2.0


def test_average_response_time_empty_list():
    assert average_response_time([]) == 0.0
