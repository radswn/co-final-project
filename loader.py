from Car import Car
from Graph import Graph
from Street import Street


def load_text_file(filename: str):
    with open(filename, mode='r') as file:
        return load_data(file.readline)


def load_stdin():
    return load_data(input)


def load_data(load_function) -> Graph:
    cars = []
    streets = dict()
    intersections = dict()

    d, i, s, v, f = map(int, load_function().split())
    for _ in range(s):
        line = load_function().split()
        b, e = map(int, line[:2])
        name = line[2]
        l = int(line[3])

        street = Street(_, name, l, b, e)
        streets[street.name] = street
        street.check_and_add(intersections)

    for _ in range(v):
        line = load_function().split()
        route = line[1:]
        cars.append(Car(_, route))

    return Graph(d, i, s, v, f, intersections, streets, cars)
