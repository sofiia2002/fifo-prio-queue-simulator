import numpy as np

class Simulator:
    def __init__(self, packet_size=1000):
        self.prev_time = 0
        self.time = 0
        self.server_status = 0
        self.num_of_delay = 0
        self.delay = 0
        self.time_busy_server = 0
        self.time_wait_in_queue = 0
        self.packet_arrival = [-1, -1]
        self.packet_process_end = -1
        self.action_type = None
        self.queue = [[],[]]
        self.packet_size = packet_size

    def get_rand_source_start_time(self, peak_rate):
        return np.random.rand() * self.packet_size/peak_rate

    def get_time_between_arrivals_exp(self, num):
        return np.random.exponential(1/num)

    def get_time_of_service_exp(self, num):
        return np.random.exponential(1/num)
    
    def get_time_between_arrivals_cbr(self, peak_rate):
        return self.packet_size/peak_rate

    def get_time_of_service_cbr(self, service_rate):
        return self.packet_size/service_rate
    
    def init_action_lists(self, lambda_val, get_time_between_arrivals):
        self.packet_arrival[0] = self.time + get_time_between_arrivals(lambda_val)
        self.packet_arrival[1] = self.get_rand_source_start_time(lambda_val) + self.time + get_time_between_arrivals(lambda_val)

    def action_a_algorithm(self, lambda_val, mi_val, get_time_of_service, get_time_between_arrivals):
        smaller_time_index = int(self.packet_arrival[0] > self.packet_arrival[1])
        self.packet_arrival[smaller_time_index] = self.time + get_time_between_arrivals(lambda_val)
        if self.server_status == 0:
            self.server_status = 1
            self.num_of_delay += 1
            time_of_service = get_time_of_service(mi_val)
            self.packet_process_end = self.time + time_of_service
        else:
            self.time_wait_in_queue += len(self.queue)*(self.time - self.prev_time)
            self.queue.append(self.time)
            self.time_busy_server += (self.time - self.prev_time)*self.server_status
    
    def action_d_algorithm(self, mi_val, get_time_of_service):
        self.time_busy_server += (self.time - self.prev_time)*self.server_status
        if len(self.queue) == 0:
            self.server_status = 0
            self.packet_process_end = -1
        else:
            self.num_of_delay += 1
            self.delay = self.delay + (self.time - self.queue[0])
            self.time_wait_in_queue += len(self.queue)*(self.time - self.prev_time)
            time_of_service = get_time_of_service(mi_val)
            self.packet_process_end = self.time + time_of_service
            self.queue.pop(0)
    
    def update_clock(self):
        self.prev_time = self.time
        smaller_time_index = int(self.packet_arrival[0] > self.packet_arrival[1])
        if (self.packet_arrival[smaller_time_index] < self.packet_process_end) or (self.packet_process_end == -1):
            self.time = self.packet_arrival[smaller_time_index]
            self.action_type = "A"
        elif (self.packet_arrival[smaller_time_index] >= self.packet_process_end):
            self.time = self.packet_process_end
            self.action_type = "D"

    def start_mm1(self, simulation_time, lambda_val, mi_val):
        self.init_action_lists(lambda_val, self.get_time_between_arrivals_exp)
        while(self.time < simulation_time):
            self.update_clock()
            if (self.action_type == "A"):
                self.action_a_algorithm(lambda_val, mi_val, self.get_time_of_service_exp, self.get_time_between_arrivals_exp)
            elif (self.action_type == "D"):
                self.action_d_algorithm(mi_val, self.get_time_of_service_exp)
        print("number of packets: ", self.num_of_delay)
        print("mean delay for client: ", self.delay/self.num_of_delay)
        print("mean clients in queue: ", self.time_wait_in_queue/self.time)
        print("server busy: ", self.time_busy_server/self.time)

    def start_fifo(self, simulation_time, bit_rate, service_rate):
        self.init_action_lists(bit_rate, self.get_time_between_arrivals_cbr)
        while(self.time < simulation_time):
            print(len(self.queue))
            print(self.queue)
            self.update_clock()
            if (self.action_type == "A"):
                self.action_a_algorithm(bit_rate, service_rate, self.get_time_of_service_cbr, self.get_time_between_arrivals_cbr)
            elif (self.action_type == "D"):
                self.action_d_algorithm(service_rate, self.get_time_of_service_cbr)
        print("number of packets: ", self.num_of_delay)
        print("mean delay for client: ", self.delay/self.num_of_delay)
        print("mean clients in queue: ", self.time_wait_in_queue/self.time)
        print("server busy: ", self.time_busy_server/self.time)