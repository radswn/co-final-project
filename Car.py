from typing import List


class Car:
    def __init__(self, id, route: List[str]):
        self.id = id
        self.route = route
        self.remaining_time = 0
        self.current_street = self.route.pop(0)

    def route_without_last(self):
        return [self.current_street] + self.route[:-1]
