from Intersection import Intersection


class Street:
    def __init__(self, id, name, time, start_id, end_id):
        self.id = id
        self.name = name
        self.time = time
        self.start_id = start_id
        self.end_id = end_id
        self.queue = []

    def check_and_add(self, intersections: dict):
        if self.start_id in intersections.keys():
            intersections.get(self.start_id).add_street_out(self.id)
        else:
            intersections[self.start_id] = Intersection(self.start_id)

        if self.end_id in intersections.keys():
            intersections.get(self.end_id).add_street_in(self.id)
        else:
            intersections[self.end_id] = Intersection(self.end_id)
