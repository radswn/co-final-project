import random
from collections import defaultdict, OrderedDict
from copy import deepcopy
from time import time

import numpy as np

from Graph import Graph
from Intersection import Intersection
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


def random_individual(graph: Graph) -> Solution:
    schedule = {}
    for intersection in graph.intersections.keys():
        streets = [s for s in graph.intersections[intersection].streets_in]
        np.random.permutation(streets)
        schedule[intersection] = {street: random.randint(1, 6) for street in streets}

    return Solution(schedule)


def mutation(sol: Solution) -> Solution:
    solution = deepcopy(sol)
    intersection = random.choice(list(solution.schedules.keys()))
    schedule = solution.schedules[intersection]
    street = random.choice(list(schedule.keys()))

    if random.random() < 0.5 and schedule[street] > 1:
        schedule[street] -= 1
    else:
        schedule[street] += 1

    return solution


def crossover(sol1: Solution, sol2: Solution) -> (Solution, Solution):
    solution1 = deepcopy(sol1)
    solution2 = deepcopy(sol2)
    child1_schedule = {}
    child2_schedule = {}

    for inter in solution1.schedules:
        # trochę uproszczona wersja crossovera, potem możemy zmienić na bardziej złożoną,
        # na razie nie chciałem zabić złożoności, więc wstępnie jest jak niżej
        child1_schedule[inter] = {street: solution1.schedules[inter][street] for street in
                                  solution2.schedules[inter].keys()}
        child2_schedule[inter] = {street: solution2.schedules[inter][street] for street in
                                  solution1.schedules[inter].keys()}

    return Solution(child1_schedule), Solution(child2_schedule)


def create_initial_population(graph: Graph):
    population = {}
    population_ratio = {}

    for _ in range(POPULATION_SIZE):
        citizen = random_individual(graph)
        population[citizen] = approximate_fitness(graph, citizen)

    denominator = sum(population.values())
    for individual in population.keys():
        population_ratio[individual] = population[individual] / denominator

    return population, population_ratio


def create_next_generation(graph, population_ratio):
    new_population = {}
    new_population_ratio = {}

    for _ in range(POPULATION_SIZE):
        parent1 = np.random.choice(list(population_ratio.keys()), p=list(population_ratio.values()))
        parent2 = np.random.choice(list(population_ratio.keys()), p=list(population_ratio.values()))

        child1, child2 = crossover(parent1, parent2)

        if random.random() < 0.2:
            child1 = mutation(child1)
        if random.random() < 0.2:
            child2 = mutation(child2)

        new_population[child1] = approximate_fitness(graph, child1)
        new_population[child2] = approximate_fitness(graph, child2)

    denominator = sum(new_population.values())
    for individual in new_population:
        new_population_ratio[individual] = new_population[individual] / denominator

    return new_population_ratio


def define_new_best(graph: Graph, best_so_far: Solution, best_score: int, candidate: Solution):
    score = approximate_fitness(graph, candidate)

    if score > best_score:
        return candidate, score
    else:
        return best_so_far, best_score


POPULATION_SIZE = 10
GENERATIONS = 10


def genetic_algorithm(graph: Graph) -> Solution:
    timer_start = time()

    population, population_ratio = create_initial_population(graph)

    best_one = random_individual(graph)
    best_score = approximate_fitness(graph, best_one)

    for _ in range(GENERATIONS):

        if not is_time_ok(timer_start):
            return best_one

        population_ratio = create_next_generation(graph, population_ratio)

        candidate_for_best = max(population_ratio, key=population_ratio.get)
        best_one, best_score = define_new_best(graph, best_one, best_score, candidate_for_best)

    return best_one


def approximate_fitness(graph: Graph, solution: Solution) -> float:
    percentage_schedules = dict()
    result = 0

    for intersection_id, schedule in solution.schedules.items():
        time_sum = sum(schedule.values())
        for street, seconds in schedule.items():
            percentage_schedules[street] = (1 / time_sum, time_sum - seconds)

    for car in graph.cars:
        expected_travel_time = 0
        route = car.full_route()

        for street in route:
            multiplier, max_waiting_time = percentage_schedules[street]
            wait_time_sum = sum([_ for _ in range(max_waiting_time + 1)])
            expected_travel_time += multiplier * wait_time_sum
            expected_travel_time += graph.streets[street].time
        expected_travel_time += graph.streets[car.route[-1]].time

        result += graph.points + (graph.duration - expected_travel_time)
    return result


def save_to_file(letter, solution: Solution):
    with open(f'solutions\\{letter}.txt', 'w+') as file:
        file.write(solution.__str__())
