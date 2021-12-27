class Car:
    def __init__(self, id, route: list):
        self.id = id
        self.route = route
        self.remaining_time = 0
        self.next = self.route.pop(0)
