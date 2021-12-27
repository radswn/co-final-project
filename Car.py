class Car:
    def __init__(self, n, route):
        self.id = n
        self.route = route
        self.next = self.route[0]
        