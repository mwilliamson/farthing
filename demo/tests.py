from nose.tools import assert_equal

import fact


def test_fib():
    test_cases = [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
    ]
    
    for index, value in test_cases:
        yield _check_fact, index, value


def _check_fact(index, value):
    assert_equal(value, fact.factorial(index))
