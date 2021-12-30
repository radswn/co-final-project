from Car import Car
from Intersection import Intersection


class Street:
    def __init__(self, id, name, time, start_id, end_id):
        self.id = id
        self.name = name
        self.time = time
        self.start_id = start_id
        self.end_id = end_id
        self.queue = [int]

    def __str__(self):
        return (f"""
    Street
      name: {self.name}
      travel_time: {self.time}
      queue: {self.queue}""")

    def setup_intersections(self, intersections: dict):
        if self.start_id in intersections.keys():
            intersections.get(self.start_id).add_street_out(self.name)
        else:
            intersections[self.start_id] = Intersection(self.start_id)

        if self.end_id in intersections.keys():
            intersections.get(self.end_id).add_street_in(self.name)
        else:
            intersections[self.end_id] = Intersection(self.end_id)

    def add_to_queue(self, car: Car):
        self.queue.append(car.id)

    def remove_from_queue(self, car: Car):
        self.queue.remove(car.id)

    def in_schedule(self, inter: Intersection):
        if self in inter.schedule.keys():
            return True

    def is_car_first_in_queue(self, car: Car):
        return self.queue[0] == car.id
