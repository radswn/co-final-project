from typing import Dict, List

from Car import Car
from Intersection import Intersection
from Solution import Solution
from Street import Street


class Graph:
    def __init__(self, d, i, s, v, f, intersections: Dict[int, Intersection], streets: Dict[str, Street],
                 cars: List[Car]):
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
        self.debug = False

        for car in self.cars:
            self.queue_car(car)

    def __str__(self):
        return (f"""
    Graph
      duration: {self.duration}
      current_time: {self.current_time}
      score: {self.score}
      cars: {''.join(car.__str__() for car in self.cars)}
      intersections: {''.join(intersection.__str__() for intersection in self.intersections.values())}
      streets: {''.join(street.__str__() for street in self.streets.values())}""")

    def queue_car(self, car: Car):
        if self.debug:
            print("Car {} moved to queue on street {}".format(car.id, car.current_street))
        self.get_cars_next_street(car).add_to_queue(car)

    def evaluate(self) -> int:
        for _ in range(self.duration):
            self.do_iteration()
        return self.score

    def do_iteration(self):
        if self.debug:
            print("Current time: {}".format(self.current_time))
        for intersection in self.intersections.values():
            if not intersection.empty_schedule():
                intersection.change_light(self.current_time)

        for car in self.cars:
            self.drive(car)

        self.current_time += 1

    def drive(self, car):
        if car.is_in_a_queue():
            if car.has_finished():
                self.end_cars_travel(car)
            else:
                current_street = self.get_cars_current_street(car)
                if self.has_green_light(current_street) and current_street.is_car_first_in_queue(car):
                    next_street = self.streets[car.get_next_street_name()]
                    self.leave_queue(car)
                    car.drive_to_next_street(next_street.time)
                    if self.debug:
                        print("Car {} drove to the next street {}".format(car.id, car.current_street))
                else:
                    if self.debug:
                        print("Car {} is waiting on street {}".format(car.id, car.current_street))
        elif car.is_approaching_queue():
            car.remaining_time -= 1
            self.queue_car(car)
        else:
            if self.debug:
                print("Car {} is riding down the {} street".format(car.id, car.current_street))
            car.remaining_time -= 1

    def has_green_light(self, street) -> bool:
        intersection = self.intersections[street.end_id]
        return intersection.current_green == street.name

    def end_cars_travel(self, car: Car):
        if self.debug:
            print("Car {} has finished".format(car.id))
        self.leave_queue(car)
        self.cars.remove(car)
        self.add_score()

    def add_score(self):
        self.score += self.points + (self.duration - self.current_time)

    def get_cars_next_street(self, car: Car) -> Street:
        return self.streets[car.current_street]

    def leave_queue(self, car: Car):
        self.get_cars_current_street(car).remove_from_queue(car)

    def get_cars_current_street(self, car: Car) -> Street:
        return self.streets[car.current_street]

    def set_priorities(self, order: int, priority_of_streets):
        for car in self.cars:
            full_route = [car.current_street] + car.route

            if car.car_is_done(order):
                continue

            priority_up(full_route[order], priority_of_streets[order])

        return priority_of_streets

    def get_longest_q_street(self, order: int, priority_of_streets):
        street_name = max(priority_of_streets[order], key=priority_of_streets[order].get)
        return self.streets[street_name]

    def set_schedules(self, solution: Solution):
        for inter_id, schedule in solution.schedules:
            self.intersections[inter_id].set_schedule(schedule)


def priority_up(street_name, priority_dict):
    priority_dict[street_name] += 1
