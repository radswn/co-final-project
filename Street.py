from Intersection import Intersection


class Street:
    def __init__(self, name, time, start_id, end_id):
        self.name = name
        self.time = time
        self.start_id = start_id
        self.end_id = end_id

    def setup_intersections(self, intersections: dict):
        if self.start_id not in intersections.keys():
            intersections[self.start_id] = Intersection(self.start_id)

        if self.end_id not in intersections.keys():
            intersections[self.end_id] = Intersection(self.end_id)
        intersections.get(self.end_id).add_street_in(self.name)
