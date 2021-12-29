from collections import defaultdict, OrderedDict
from math import ceil
from time import time

from Graph import Graph
from Solution import Solution

TIME_LIMIT = 300


def greedy(graph: Graph) -> Solution:
    timer_start = time()
    longest_route = get_longest_route(graph)
    priority_of_streets = [defaultdict(int) for _ in range(longest_route)]

    for order in range(longest_route):
        if not is_time_ok(timer_start):
            break

        priority_of_streets = graph.set_priorities(order, priority_of_streets)
        scheduling(graph, order, priority_of_streets)

    return Solution(graph.intersections)


def migrate_values(inter, street, order: int, priority_of_streets, value):
    if len(inter.schedule) >= order + 1 and order + 1 < len(priority_of_streets):
        priority_of_streets[order + 1][street.name] = value
        return True
    return False


def scheduling(graph: Graph, order: int, priority_of_streets):
    while len(priority_of_streets[order]) > 0:
        street = graph.get_longest_q_street(order, priority_of_streets)
        value = priority_of_streets[order].pop(street.name)
        inter = graph.intersections[street.end_id]

        if street.in_schedule(inter):
            continue
        elif migrate_values(inter, street, order, priority_of_streets, value):
            continue
        else:
            inter.schedule[street] = value


def is_time_ok(timer_start) -> bool:
    return time() <= timer_start + TIME_LIMIT


def get_longest_route(graph: Graph):
    return max(len([car.current_street] + car.route) for car in graph.cars)


def greedy2(graph: Graph):
    street_appearance_count = defaultdict(int)

    for car in graph.cars:
        for street_name in car.full_route():
            street_appearance_count[street_name] += 1

    for intersection in graph.intersections.values():
        schedule = OrderedDict()

        for street_in in intersection.streets_in:
            appearances = street_appearance_count[street_in]
            if appearances > 0:
                schedule[street_in] = ceil(appearances / 2)

        intersection.set_schedule(schedule)

    return Solution(graph.intersections)


def sophisticated():
    ...
