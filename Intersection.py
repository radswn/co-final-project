class Intersection:
    def __init__(self, id):
        self.id = id
        self.schedule = dict()
        self.streets_in = []
        self.streets_out = []

    def add_street_in(self, street_id):
        self.streets_in.append(street_id)

    def add_street_out(self, street_id):
        self.streets_out.append(street_id)