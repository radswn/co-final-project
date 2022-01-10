from Car import Car
from Solution import Solution


def run_all_tests():
    should_create_correct_solution()
    should_return_correct_path()


def should_return_correct_path():
    car = Car(0, ['a', 'b', 'c'])
    assert car.full_route() == ['a', 'b']


def should_create_correct_solution():
    solution = Solution({0: {'abc': 2, 'bcd': 3}, 1: {'cde': 1, 'def': 4}})
    print(solution)
