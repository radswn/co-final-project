from collections import OrderedDict


class Intersection:
    def __init__(self, id):
        self.id = id
        self.schedule = OrderedDict()
        self.streets_in = []
        self.current_green = None
        self.timetable = []
        self.period = 0

    def __str__(self):
        return (f"""
    Intersection
      id: {self.id}
      schedule: {' '.join(k + ': ' + str(v) for k, v in self.schedule.items())}
      streets_in: {' '.join(self.streets_in)}
      timetable: {' '.join(self.timetable)}
      current_green: {self.current_green}""")

    def add_street_in(self, street_name):
        self.streets_in.append(street_name)

    def set_schedule(self, schedule: OrderedDict):
        self.schedule = schedule
        self.period = sum(schedule.values())
        [self.timetable.extend([k] * v) for k, v in schedule.items()]
        if len(self.timetable) > 0:
            self.current_green = self.timetable[0]

    def change_light(self, current_time):
        current_period_time = current_time % self.period
        self.current_green = self.timetable[current_period_time]
