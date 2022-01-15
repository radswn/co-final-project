import math
import random
from collections import OrderedDict, defaultdict
from copy import deepcopy
from time import time

import numpy as np

from Graph import Graph
from Solution import Solution

TIME_LIMIT = 300
POPULATION_SIZE = 20
GENERATIONS = 20
HC_NEIGHBORS = 10
MUTATION_PROBABILITY = 0.2


def is_time_ok(timer_start) -> bool:
    return time() <= timer_start + TIME_LIMIT


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


def hill_climbing(graph: Graph) -> Solution:
    timer_start = time()
    current_solution = get_state_zero(graph)
    best_score = approximate_fitness(graph, current_solution)
    current_score = best_score
    best_solution = deepcopy(current_solution)

    while True:
        for _ in range(HC_NEIGHBORS):
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


def genetic_algorithm(graph: Graph) -> Solution:
    timer_start = time()
    streets_appearance_count = counting_streets(graph)
    population, population_ratio = create_initial_population(graph, streets_appearance_count)

    best_one = random_individual(graph, streets_appearance_count)
    best_score = approximate_fitness(graph, best_one)

    for _ in range(GENERATIONS):
        if not is_time_ok(timer_start):
            return best_one

        population_ratio = create_next_generation(graph, population_ratio)

        candidate_for_best = max(population_ratio, key=population_ratio.get)
        best_one, best_score = define_new_best(graph, best_one, best_score, candidate_for_best)

    return best_one


def counting_streets(graph: Graph):
    street_appearance_count = defaultdict(int)
    for car in graph.cars:
        for street_name in car.route_without_last():
            street_appearance_count[street_name] += 1
    return street_appearance_count


def random_individual(graph: Graph, street_appearance_count) -> Solution:
    schedule = {}
    for intersection in graph.intersections.keys():
        streets = [s for s in graph.intersections[intersection].streets_in]
        np.random.permutation(streets)
        schedule[intersection] = {street: math.floor(math.log2(street_appearance_count[street])) for street in
                                  street_appearance_count.keys()}
    return Solution(schedule)


def mutation(sol: Solution) -> Solution:
    solution = deepcopy(sol)
    intersection = random.choice(
        [inter_id for inter_id, schedule in solution.schedules.items() if len(schedule.keys()) > 1])
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

    for _, (inter_k, inter_v) in enumerate(solution1.schedules.items()):
        if _ < len(solution1.schedules.keys()):
            child1_schedule[inter_k] = solution1.schedules[inter_k]
            child2_schedule[inter_k] = solution2.schedules[inter_k]
        else:
            child1_schedule[inter_k] = solution2.schedules[inter_k]
            child2_schedule[inter_k] = solution1.schedules[inter_k]

    return Solution(child1_schedule), Solution(child2_schedule)


def create_initial_population(graph: Graph, streets_appearance_count):
    population = {}
    population_ratio = {}

    for _ in range(POPULATION_SIZE):
        citizen = random_individual(graph, streets_appearance_count)
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

        if random.random() < MUTATION_PROBABILITY:
            child1 = mutation(child1)
        if random.random() < MUTATION_PROBABILITY:
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


def approximate_fitness(graph: Graph, solution: Solution) -> float:
    percentage_schedules = dict()
    result = 0

    for intersection_id, schedule in solution.schedules.items():
        time_sum = sum(schedule.values())
        for street, seconds in schedule.items():
            percentage_schedules[street] = (1 / time_sum, time_sum - seconds)

    for car in graph.cars:
        expected_travel_time = 0
        route = car.route_without_last()

        for street in route:
            multiplier, max_waiting_time = percentage_schedules[street]
            wait_time_sum = sum([_ for _ in range(max_waiting_time + 1)])

            expected_travel_time += multiplier * wait_time_sum
            if street != car.current_street:
                expected_travel_time += graph.streets[street].time

        expected_travel_time += graph.streets[car.route[-1]].time

        result += max(graph.points + (graph.duration - expected_travel_time), 1)
    return result


def save_to_file(letter, solution: Solution):
    with open(f'solutions\\{letter}.txt', 'w+') as file:
        file.write(solution.__str__())
