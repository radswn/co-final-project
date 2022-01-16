from typing import List


class Car:
    def __init__(self, id, route: List[str]):
        self.id = id
        self.route = route
        self.remaining_time = 0
