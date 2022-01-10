from collections import defaultdict, OrderedDict
from time import time
from copy import deepcopy
import random

from Graph import Graph
from Solution import Solution
from Street import Street
from Intersection import Intersection
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
    for intersection in graph.intersections.values():
        if intersection.schedule != {}:
            intersection.set_schedule(intersection.schedule)

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
            inter.schedule[street.name] = value


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
                schedule[street_in] = appearances

        intersection.set_schedule(schedule)

    return Solution(graph.intersections)


def get_state_zero(graph: Graph) -> Solution:
    schedule = {}
    for intersection in graph.intersections.keys():
        schedule[intersection] = OrderedDict()
        for street_in in graph.intersections[intersection].streets_in:
            schedule[intersection][street_in] = 1
    return Solution(schedule)


def random_neighbour(sol: Solution) -> Solution:
    solution = deepcopy(sol)
    intersection = random.choice(list(solution.schedules.keys()))
    schedule = solution.schedules[intersection]
    street = random.choice(list(schedule.keys()))
    schedule[street] += 1
    return solution


def reverse_changes(graph: Graph, intersection: Intersection, street):
    schedule = intersection.schedule
    schedule[street] -= 1
    intersection.set_schedule(schedule)


def hill_climbing(graph: Graph) -> Solution:
    timer_start = time()
    solution_zero = get_state_zero(graph)
    best_score = approximate_fitness(graph, solution_zero)
    current_solution = solution_zero
    current_score = best_score
    best_solution = deepcopy(current_solution)
    while True:
        for _ in range(10):

            if not is_time_ok(timer_start):
                return current_solution

            neighbour = random_neighbour(current_solution)
            neighbour_score = approximate_fitness(graph, neighbour)

            if neighbour_score > best_score:
                best_score = neighbour_score
                best_solution = neighbour

        if current_score == best_score:
            return current_solution
        else:
            current_score = best_score
            current_solution = best_solution


def sophisticated():
    ...


def approximate_fitness(graph: Graph, solution: Solution) -> float:
    percentage_schedules = dict()
    result = 0

    for intersection_id, schedule in solution.schedules.items():
        time_sum = sum(schedule.values())
        for street, seconds in schedule.items():
            percentage_schedules[street] = seconds / time_sum
    # print(percentage_schedules)
    for car in graph.cars:
        route = car.full_route()
        chance_for_passing = 1
        for street in route:
            chance_for_passing *= percentage_schedules[street]
        result += chance_for_passing * graph.points

    return result
