from time import time

from Graph import Graph

TIME_LIMIT = 300


def set_priorities(graph: Graph, order: int, priority_of_streets):
    # iterate through all cars' routes and add order-th position to order-th dict
    for car in graph.cars:
        full_route = [car.current_street] + car.route
        if len(full_route) <= order + 1:
            continue
        if full_route[order] in priority_of_streets[order].keys():
            priority_of_streets[order][full_route[order]] += 1
        else:
            priority_of_streets[order][full_route[order]] = 1
    return priority_of_streets


def scheduling(graph: Graph, order: int, priority_of_streets):
    # add streets to schedules or add their value to next dict
    while len(priority_of_streets[order]) > 0:
        # get the street with the longest que
        street_name = max(priority_of_streets[order], key=priority_of_streets[order].get)
        street = graph.streets[street_name]
        value = priority_of_streets[order].pop(street.name)
        # get intersection of this street
        inter = graph.intersections[street.end_id]

        # check if the street is already in the schedule
        if street in inter.schedule.keys():
            continue
        # if we already added street in this iteration - add its value (queue) to the next iteration
        if len(inter.schedule) >= order + 1:
            priority_of_streets[order + 1][street.name] = value

        # add street to the schedule
        inter.schedule[street] = value


def greedy(graph: Graph):
    timer_start = time()

    # może damy tu while TRUE albo coś, bo to sprawdzanie time limitu w tym miejscu chuja daje xd
    while time() <= timer_start + TIME_LIMIT:
        longest_route = max(len([car.current_street] + car.route) for car in graph.cars)
        # make as many dictionaries as long is the longest route
        priority_of_streets = [dict() for _ in range(longest_route)]
        for order in range(longest_route):
            if time() > timer_start + TIME_LIMIT:
                break
            # set priorities for streets - how many cars have street XYZ as their destination in order-th position
            # this will determine the order of streets in the schedules
            priority_of_streets = set_priorities(graph, order, priority_of_streets)

            scheduling(graph, order, priority_of_streets)
        break


def sophisticated():
    ...
