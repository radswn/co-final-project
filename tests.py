from collections import OrderedDict

from Solution import Solution
from algorithms import sort_schedule


def run_all_tests():
    should_create_correct_solution()
    should_sort_schedule()


def should_create_correct_solution():
    solution = Solution({0: {'abc': 2, 'bcd': 3}, 1: {'cde': 1, 'def': 4}})
    assert solution.__str__() == "2\n0\n2\nabc 2\nbcd 3\n1\n2\ncde 1\ndef 4\n"


def should_sort_schedule():
    order = {'a': 1, 'b': 2, 'c': 0}
    schedule = OrderedDict({'b': 1, 'a': 1, 'c': 1})
    assert sort_schedule(order, schedule) == {'c': 1, 'a': 1, 'b': 1}
