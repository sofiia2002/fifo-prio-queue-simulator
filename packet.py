class Packet:
    def __init__(self, time_of_arrival, priority, time_to_process) :
        self.time_of_arrival = time_of_arrival
        self.priority = priority
        self.time_to_process = time_to_process