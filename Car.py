class Car:
    def __init__(self, id, route: list):
        self.id = id
        self.route = route
        self.remaining_time = 0
        self.current_street = self.route.pop(0)

    def __str__(self):
        return (f"""
    Car:
      id: {self.id}
      current_street: {self.current_street}
      time_to_intersection: {self.remaining_time}
      route: {self.route}""")

    def full_route(self):
        return [self.current_street] + self.route

    def has_finished(self) -> bool:
        return len(self.route) == 0 and self.remaining_time == 0

    def drive_to_next_street(self, next_street_travel_time):
        self.current_street = self.route.pop(0)
        self.remaining_time = next_street_travel_time

    def get_next_street_name(self):
        return self.route[0]

    def is_in_a_queue(self) -> bool:
        return self.remaining_time == 0

    def is_approaching_queue(self) -> bool:
        return self.remaining_time == 1

    def car_is_done(self, order):
        return len(self.route) <= order
