from collections import OrderedDict


class Intersection:
    def __init__(self, id):
        self.id = id
        self.schedule = OrderedDict()
        self.streets_in = [str]
        self.streets_out = [str]
        self.current_green = None
        self.timetable = [str]
        self.period = 0

    def __str__(self):
        return (f"""
    Intersection
      id: {self.id}
      schedule: {self.schedule.items()}
      streets_in: {self.streets_in}
      current_green: {self.current_green}""")

    def add_street_in(self, street_name):
        self.streets_in.append(street_name)

    def add_street_out(self, street_name):
        self.streets_out.append(street_name)

    def set_schedule(self, schedule: OrderedDict):
        self.schedule = schedule
        self.period = sum(schedule.values())
        [self.timetable.extend([k] * v) for k, v in schedule.items()]

    def change_light(self, current_time):
        current_period_time = current_time % self.period
        self.current_green = self.timetable[current_period_time]

    def empty_schedule(self) -> bool:
        return self.schedule == {}
