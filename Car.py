class Car:
    def __init__(self, id, route):
        self.id = id
        self.route = route
        self.next = self.route[0]
        