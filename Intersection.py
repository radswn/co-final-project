class Intersection:
    def __init__(self, id):
        self.id = id
        self.schedule = dict()
        self.streets_in = []
        self.streets_out = []
        self.current_green = None

    def add_street_in(self, street_name):
        self.streets_in.append(street_name)

    def add_street_out(self, street_name):
        self.streets_out.append(street_name)
