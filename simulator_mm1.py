import numpy as np

class Simulator:
    def __init__(self):
        self.prev_time = 0
        self.time = 0
        self.server_status = 0
        self.num_of_delay = 0
        self.delay = 0
        self.time_busy_server = 0
        self.time_wait_in_queue = 0
        self.packet_arrival = -1
        self.packet_process_end = -1
        self.action_type = None
        self.queue = []

    def get_time_between_arrivals(self, num):
        return np.random.exponential(1/num)

    def get_time_of_service(self, num):
        return np.random.exponential(1/num)
    
    def init_action_lists(self, lambda_val):
        packet_arival = self.get_time_between_arrivals(lambda_val)
        self.packet_arrival = self.time + packet_arival

    def action_a_algorithm(self, lambda_val, mi_val):
        packet_arival = self.get_time_between_arrivals(lambda_val)
        self.packet_arrival = self.time + packet_arival
        if self.server_status == 0:
            self.server_status = 1
            self.num_of_delay += 1
            time_of_service = self.get_time_of_service(mi_val)
            self.packet_process_end = self.time + time_of_service
        else:
            self.time_wait_in_queue += len(self.queue)*(self.time - self.prev_time)
            self.queue.append(self.time)
            self.time_busy_server += (self.time - self.prev_time)*self.server_status
    
    def action_d_algorithm(self, mi_val):
        if len(self.queue) == 0:
            self.server_status = 0
            self.packet_process_end = -1
            self.time_busy_server += (self.time - self.prev_time)*self.server_status
        else:
            self.num_of_delay += 1
            self.delay = self.delay + (self.time - self.queue[0])
            self.time_wait_in_queue += len(self.queue)*(self.time - self.prev_time)
            time_of_service = self.get_time_of_service(mi_val)
            self.packet_process_end = self.time + time_of_service
            self.queue.pop(0)
            self.time_busy_server += (self.time - self.prev_time)*self.server_status
    
    def update_clock(self):
        self.prev_time = self.time
        if (self.packet_arrival < self.packet_process_end) or (self.packet_process_end == -1):
            self.time = self.packet_arrival
            self.action_type = "A"
        elif (self.packet_arrival > self.packet_process_end):
            self.time = self.packet_process_end
            self.action_type = "D"

    def start_mm1(self, simulation_time, lambda_val, mi_val):
        self.init_action_lists(lambda_val)
        while(self.time < simulation_time):
            self.update_clock()
            if (self.action_type == "A"):
                self.action_a_algorithm(lambda_val, mi_val)
            elif (self.action_type == "D"):
                self.action_d_algorithm(mi_val)
        print("number of packets: ", self.num_of_delay)
        print("mean delay for client: ", self.delay/self.num_of_delay)
        print("mean clients in queue: ", self.time_wait_in_queue/self.time)
        print("server busy: ", self.time_busy_server/self.time)