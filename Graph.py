from typing import Dict, Set

from Car import Car
from Intersection import Intersection
from Street import Street


class Graph:
    def __init__(self, d, i, s, v, f, intersections: Dict[int, Intersection], streets: Dict[str, Street],
                 cars: Set[Car]):
        self.duration = d
        self.intersections_nr = i
        self.streets_nr = s
        self.cars_nr = v
        self.points = f
        self.intersections = intersections
        self.streets = streets
        self.cars = cars
