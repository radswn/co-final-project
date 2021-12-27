from Intersection import Intersection


class Solution:
    def __init__(self, a: int, intersections: dict[int, Intersection]):
        self.a = a
        self.schedules = [(k, len(v.schedule), v.schedule) for k, v in intersections.items()]

    def __str__(self):
        solution = str(self.a) + '\n'

        for intersection_id, inc_streets_num, schedule in self.schedules:
            solution += str(intersection_id) + '\n' + str(inc_streets_num) + '\n'

            for plan in schedule:
                solution += " ".join(plan) + '\n'

        return solution
