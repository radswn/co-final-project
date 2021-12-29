class Car:
    def __init__(self, id, route: list):
        self.id = id
        self.route = route
        self.remaining_time = 0
        self.current_street = self.route.pop(0)

    def has_finished(self):
        return len(self.route) == 0

    def drive_to_next_street(self, next_street_travel_time):
        self.current_street = self.route.pop(0)
        self.remaining_time = next_street_travel_time

    def get_next_street_name(self):
        return self.route[0]

    def is_in_a_queue(self):
        return self.remaining_time == 0

    def is_approaching_queue(self):
        return self.remaining_time == 1
