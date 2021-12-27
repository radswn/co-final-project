from time import time

from Graph import Graph

TIME_LIMIT = 300


def greedy(graph: Graph):
    timer_start = time()

    while graph.cars and time() <= timer_start + TIME_LIMIT:
        iterations = graph.duration
        # SUBTRACT ITERATIONS
        while iterations > 0:
            # priority dict - how many cars queued right now
            priority_dict = dict()
            for street_key in graph.streets.keys():
                priority_dict[street_key] = len(graph.streets[street_key].queue)

            while priority_dict:
                street = graph.streets[max(priority_dict, key=priority_dict.get)]
                street_time = priority_dict[street.name]

                if street.name in graph.intersections[street.end_id].schedule.keys():
                    priority_dict.pop(street.name)
                    continue

                graph.intersections[street.end_id].schedule[street.name] = street_time
                priority_dict.pop(street.name)

            # move cars


def sophisticated():
    ...


def simulate_iteration(graph: Graph):
    ...
