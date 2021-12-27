class Graph:
    def __init__(self, d, i, s, v, f, intersections: dict, streets: dict, cars: list):
        self.duration = d
        self.intersections_nr = i
        self.streets_nr = s
        self.car_nr = v
        self.points = f
        self.intersections = intersections
        self.streets = streets
        self.cars = cars
        # queue up cars
        for car in self.cars:
            self.streets[car.next].queue.append(car.id)
