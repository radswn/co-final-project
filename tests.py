from Car import Car
from Solution import Solution


def run_all_tests():
    should_create_correct_solution()
    should_return_correct_path()


def should_return_correct_path():
    car = Car(0, ['a', 'b', 'c'])
    assert car.current_street == 'a'
    assert car.full_route() == ['a', 'b']


def should_create_correct_solution():
    solution = Solution({0: {'abc': 2, 'bcd': 3}, 1: {'cde': 1, 'def': 4}})
    assert solution.__str__() == "2\n0\n2\nabc 2\nbcd 3\n1\n2\ncde 1\ndef 4\n"
