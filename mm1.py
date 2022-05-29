import numpy as np
class Simulator:
    def __init__(self):
        self.number_of_packets_in_queue = 0
        self.clock = 0.0
        self.time_of_arrival = self.get_time_between_arrivals()
        self.time_of_departure = float('inf')
        self.total_delay = 0
        self.total_clients_served = 0
        # figure these out
        self.delay_per_client = 0
        self.server_usage = 0
        self.clients_in_queue = 0

    def get_time_between_arrivals(self):
        return np.random.exponential(1. / 3)

    def get_time_of_service(self):
        return np.random.exponential(1. / 4)

    def process_time(self):
        time_of_next_event = min(self.time_of_arrival, self.time_of_departure)
        # total czas oczekiwania - dla kazdego eventu liczymy sume od wszystkich pakietow
        self.total_delay += self.number_of_packets_in_queue * (time_of_next_event - self.clock)
        self.clock = time_of_next_event

        if self.time_of_arrival <= self.time_of_departure:
            self.process_new_client()
        else:
            self.process_new_departure()

    def process_new_client(self):
        self.number_of_packets_in_queue += 1
        if self.number_of_packets_in_queue <= 1:
            self.time_of_departure = self.clock + self.get_time_of_service()
        self.time_of_arrival = self.clock + self.get_time_between_arrivals()

    def process_new_departure(self):
        self.total_clients_served += 1
        self.number_of_packets_in_queue -= 1
        if self.number_of_packets_in_queue > 0:
            self.time_of_departure = self.clock + self.get_time_of_service()


if __name__ == "__main__":
    sim = Simulator()
    for i in range(1000):
        sim.process_time()
    print("srednie opoznenie dla klienta: " + str(sim.total_delay / sim.total_clients_served))