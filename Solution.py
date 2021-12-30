from Intersection import Intersection


class Solution:
    def __init__(self, intersections: dict[int, Intersection]):
        self.a = sum([1 for inter in intersections.values() if inter.schedule != {}])
        self.schedules = [(k, len(v.schedule), v.schedule) for k, v in intersections.items()]

    def __str__(self):
        solution = str(self.a) + '\n'

        for intersection_id, inc_streets_num, schedule in self.schedules:
            if schedule != {}:
                solution += str(intersection_id) + '\n' + str(inc_streets_num) + '\n'

                for name, duration in schedule.items():
                    solution += name + ' ' + str(duration) + '\n'

        return solution
