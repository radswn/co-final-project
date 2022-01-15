from collections import OrderedDict


class Intersection:
    def __init__(self, id):
        self.id = id
        self.schedule = OrderedDict()
        self.streets_in = []

    def add_street_in(self, street_name):
        self.streets_in.append(street_name)
