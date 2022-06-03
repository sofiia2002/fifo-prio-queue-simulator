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
        self.packet_arrival = [-1, -1]
        self.packet_process_end = -1
        self.action_type = None
        self.queue_source = []
        self.queue = []

    def get_rand_source_start_time(self, peak_rate, packet_size):
        #peak_rate -> number, packet_size -> number
        return np.random.rand() * packet_size/peak_rate
    
    def get_time_between_arrivals_cbr(self, peak_rate, packet_size):
        #peak_rate -> number, packet_size -> number
        return packet_size/peak_rate

    def get_time_of_service_cbr(self, service_rate, packet_size):
        #service_rate -> number, packet_size -> number
        return packet_size/service_rate
    
    def init_action_lists(self, peak_rate, packet_size, get_time_between_arrivals):
        #peak_rate -> [<source1>, <source2>], packet_size -> [<source1>, <source2>], get_time_between_arrivals -> void
        self.packet_arrival[0] = self.time + get_time_between_arrivals(peak_rate[0], packet_size[0])
        self.packet_arrival[1] = self.time + self.get_rand_source_start_time(peak_rate[0], packet_size[0]) + get_time_between_arrivals(peak_rate[1], packet_size[1])

    def action_a_algorithm(self, peak_rate, packet_size, service_rate, get_time_of_service, get_time_between_arrivals):
        #peak_rate -> [<source1>, <source2>], packet_size -> [<source1>, <source2>], service_rate -. nnumber, get_time_between_arrivals -> void, get_time_of_service -> void
        smaller_time_index = int(self.packet_arrival[0] > self.packet_arrival[1])
        self.packet_arrival[smaller_time_index] = self.time + get_time_between_arrivals(peak_rate[smaller_time_index], packet_size[smaller_time_index])
        if self.server_status == 0:
            self.server_status = 1
            self.num_of_delay += 1
            time_of_service = get_time_of_service(service_rate, packet_size[smaller_time_index])
            self.packet_process_end = self.time + time_of_service
        else:
            self.time_wait_in_queue += len(self.queue)*(self.time - self.prev_time)
            self.queue.append(self.time)
            self.queue_source.append(smaller_time_index)
            self.time_busy_server += (self.time - self.prev_time)*self.server_status
    
    def action_d_algorithm(self, service_rate, packet_size, get_time_of_service):
        #packet_size -> [<source1>, <source2>], service_rate -. nnumber, get_time_of_service -> void
        self.time_busy_server += (self.time - self.prev_time)*self.server_status
        if len(self.queue) == 0:
            self.server_status = 0
            self.packet_process_end = -1
        else:
            self.num_of_delay += 1
            self.delay = self.delay + (self.time - self.queue[0])
            self.time_wait_in_queue += len(self.queue)*(self.time - self.prev_time)
            time_of_service =  get_time_of_service(service_rate, packet_size[self.queue_source[0]])
            self.packet_process_end = self.time + time_of_service
            self.queue.pop(0)
            self.queue_source.pop(0)
    
    def update_clock(self):
        self.prev_time = self.time
        smaller_time_index = int(self.packet_arrival[0] > self.packet_arrival[1])
        if (self.packet_arrival[smaller_time_index] < self.packet_process_end) or (self.packet_process_end == -1):
            self.time = self.packet_arrival[smaller_time_index]
            self.action_type = "A"
        elif (self.packet_arrival[smaller_time_index] >= self.packet_process_end):
            self.time = self.packet_process_end
            self.action_type = "D"

    def start_fifo(self, simulation_time: int, bit_rate: list, packet_size: list, service_rate: int): 
        #bit_rate -> [<source1>, <source2>], packet_size -> [<source1>, <source2>], service_rate -> value
        self.init_action_lists(bit_rate, packet_size, self.get_time_between_arrivals_cbr)
        while(self.time < simulation_time):
            print(len(self.queue))
            print(self.queue)
            self.update_clock()
            if (self.action_type == "A"):
                self.action_a_algorithm(bit_rate, packet_size, service_rate, self.get_time_of_service_cbr, self.get_time_between_arrivals_cbr)
            elif (self.action_type == "D"):
                self.action_d_algorithm(service_rate, packet_size, self.get_time_of_service_cbr)
        print("number of packets: ", self.num_of_delay)
        print("mean delay for client: ", self.delay/self.num_of_delay)
        print("mean clients in queue: ", self.time_wait_in_queue/self.time)
        print("server busy: ", self.time_busy_server/self.time)