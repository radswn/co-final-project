from Car import Car
from Intersection import Intersection
from Street import Street


class Graph:
    def __init__(self, d, i, s, v, f, intersections: dict[int, Intersection], streets: dict[str, Street],
                 cars: list[Car]):
        self.duration = d
        self.intersections_nr = i
        self.streets_nr = s
        self.cars_nr = v
        self.points = f
        self.intersections = intersections
        self.streets = streets
        self.cars = cars
        self.score = 0
        self.current_time = 0

        for car in self.cars:
            self.queue_car(car)

    def queue_car(self, car: Car):
        self.get_cars_next_street(car).add_to_queue(car)

    def evaluate(self) -> int:
        for _ in range(self.duration):
            self.do_iteration()
        return self.score

    def do_iteration(self):
        for intersection in self.intersections.values():
            intersection.change_light(self.current_time)

        for car in self.cars:
            self.drive(car)

        self.current_time += 1

    def drive(self, car):
        if car.is_in_a_queue():
            if car.has_finished():
                self.end_cars_travel(car)
            elif self.has_green_light(self.get_cars_current_street(car)):
                next_street = self.streets[car.get_next_street_name()]
                self.leave_queue(car)
                car.drive_to_next_street(next_street.time)
        else:
            if car.is_approaching_queue():
                self.queue_car(car)
            car.remaining_time -= 1

    def has_green_light(self, street) -> bool:
        intersection = self.intersections[street.end_id]
        return intersection.current_green == street.name

    def end_cars_travel(self, car: Car):
        self.cars.remove(car)
        self.leave_queue(car)
        self.add_score()

    def add_score(self):
        self.score += self.points + (self.duration - self.current_time)

    def get_cars_next_street(self, car: Car) -> Street:
        return self.streets[car.get_next_street_name()]

    def leave_queue(self, car: Car):
        self.get_cars_current_street(car).remove_from_queue(car)

    def get_cars_current_street(self, car: Car) -> Street:
        return self.streets[car.current_street]
