from time import time

from Graph import Graph

TIME_LIMIT = 300


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


def time_is_ok(timer_start):
    if time() > timer_start + TIME_LIMIT:
        return


def get_longest_route(graph: Graph):
    return max(len([car.current_street] + car.route) for car in graph.cars)


def greedy(graph: Graph):
    timer_start = time()

    longest_route = get_longest_route(graph)

    priority_of_streets = [dict() for _ in range(longest_route)]
    for order in range(longest_route):
        time_is_ok(timer_start)

        priority_of_streets = graph.set_priorities(order, priority_of_streets)

        scheduling(graph, order, priority_of_streets)


def sophisticated():
    ...
