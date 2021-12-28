from time import time

from Graph import Graph

TIME_LIMIT = 300


def greedy(graph: Graph):
    timer_start = time()

    while time() <= timer_start + TIME_LIMIT:
        iterations = graph.duration
        longest_route = max(len(car.route) for car in graph.cars)
        # make as many dictionaries as long is the longest route
        priority_of_streets = [dict() for _ in range(longest_route)]
        for order in range(longest_route):
            # iterate through all cars' routes and add order-th position to order-th dict
            for car in graph.cars:
                if len(car.route) <= order+1:
                    continue
                if car.route[order] in priority_of_streets[order].keys():
                    priority_of_streets[order][car.route[order]] += 1
                else:
                    priority_of_streets[order][car.route[order]] = 1
            # add streets to schedules or add their value to next dict
            while len(priority_of_streets[order]) > 0:
                street_name = max(priority_of_streets[order], key=priority_of_streets[order].get)
                street = graph.streets[street_name]
                value = priority_of_streets[order].pop(street.name)
                inter = graph.intersections[street.end_id]
                # check if the street is already in the schedule; we add only one street at the time
                if street in inter.schedule.keys():
                    continue
                if len(inter.schedule) >= order + 1:
                    priority_of_streets[order + 1][street.name] = value
                # add street to teh schedule
                inter.schedule[street] = value
        break





        # SUBTRACT ITERATIONS
        # while iterations > 0:
        #     # priority dict - how many cars queued right now
        #     priority_dict = dict()
        #     for street_key in graph.streets.keys():
        #         priority_dict[street_key] = len(graph.streets[street_key].queue)
        #
        #     while priority_dict:
        #         street = graph.streets[max(priority_dict, key=priority_dict.get)]
        #         street_time = priority_dict[street.name]
        #
        #         if street.name in graph.intersections[street.end_id].schedule.keys():
        #             priority_dict.pop(street.name)
        #             continue
        #
        #         graph.intersections[street.end_id].schedule[street.name] = street_time
        #         priority_dict.pop(street.name)


def sophisticated():
    ...


def simulate_iteration(graph: Graph):
    ...
