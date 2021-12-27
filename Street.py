class Street:
    def __init__(self, id, name, fixed_time, inter_start, inter_end):
        self.id = id
        self.name = name
        self.fixed_time = fixed_time
        self.inter_start = inter_start
        self.inter_end = inter_end
        self.queue = []
