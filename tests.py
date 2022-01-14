from collections import OrderedDict

from Car import Car
from Graph import Graph
from Intersection import Intersection
from Solution import Solution
from Street import Street


def run_all_tests():
    should_create_correct_solution()
    should_return_correct_route()
    should_evaluate_test_correctly()


def should_evaluate_test_correctly():
    intersections = {
        0: Intersection(0),
        1: Intersection(1),
        2: Intersection(2),
        3: Intersection(3)
    }
    intersections[0].add_street_in('rue-de-londres')

    intersections[1].add_street_in('rue-d-amsterdam')
    intersections[1].add_street_in('rue-d-athenes')

    intersections[2].add_street_in('rue-de-moscou')

    intersections[3].add_street_in('rue-de-rome')

    streets = {
        'rue-de-londres': Street('rue-de-londres', 1, 2, 0),
        'rue-d-amsterdam': Street('rue-d-amsterdam', 1, 0, 1),
        'rue-d-athenes': Street('rue-d-athenes', 1, 3, 1),
        'rue-de-rome': Street('rue-de-rome', 2, 2, 3),
        'rue-de-moscou': Street('rue-de-moscou', 3, 1, 2)
    }

    cars = {
        Car(0, 'rue-de-londres rue-d-amsterdam rue-de-moscou rue-de-rome'.split()),
        Car(1, 'rue-d-athenes rue-de-moscou rue-de-londres'.split())
    }

    graph = Graph(6, 4, 5, 2, 1000, intersections, streets, cars)

    schedules = {
        1: OrderedDict({
            'rue-d-athenes': 2,
            'rue-d-amsterdam': 1
        }),
        0: OrderedDict({
            'rue-de-londres': 2
        }),
        2: OrderedDict({
            'rue-de-moscou': 1
        })
    }

    example_solution = Solution(schedules)

    result = graph.evaluate(example_solution)
    assert result == 1002


def should_return_correct_route():
    car = Car(0, ['a', 'b', 'c'])
    assert car.current_street == 'a'
    assert car.route_without_last() == ['a', 'b']


def should_create_correct_solution():
    solution = Solution({0: {'abc': 2, 'bcd': 3}, 1: {'cde': 1, 'def': 4}})
    assert solution.__str__() == "2\n0\n2\nabc 2\nbcd 3\n1\n2\ncde 1\ndef 4\n"
