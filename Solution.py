from typing import Dict


class Solution:
    def __init__(self, schedules: Dict[int, Dict[str, int]]):
        self.a = sum([1 for schedule in schedules.values() if schedule != {}])
        self.schedules = schedules

    def __str__(self):
        solution = str(self.a) + '\n'

        for intersection_id, schedule in self.schedules:
            if schedule != {}:
                solution += str(intersection_id) + '\n' + str(len(schedule.values())) + '\n'

                for name, duration in schedule.items():
                    solution += name + ' ' + str(duration) + '\n'

        return solution
