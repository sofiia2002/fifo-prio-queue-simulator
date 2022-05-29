from packet import Packet
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

    def generate_packet_mm1(self, bit_rate):        
        return np.random.exponential(1. / 3), np.random.exponential(1. / 4)
    
    def init_action_lists(self, bit_rate):
        packet_arival, _ = self.generate_packet_mm1(bit_rate)
        self.packet_arrival = self.time + packet_arival

    def action_a_algorithm(self, bit_rate, processing_rate):
        packet_arival, packet_length = self.generate_packet_mm1(bit_rate)
        self.packet_arrival = self.time + packet_arival
        if self.server_status == 0:
            self.num_of_delay = self.num_of_delay + 1
            self.server_status = 1
            self.packet_process_end = self.time + packet_length
        else:
            self.queue.append(self.time)
        self.time_busy_server = self.time_busy_server + (self.time - self.prev_time)*self.server_status
        self.time_wait_in_queue = self.time_wait_in_queue + len(self.queue)*(self.time - self.prev_time)
    
    def action_d_algorithm(self, bit_rate, processing_rate):
        if len(self.queue) == 0:
            self.server_status = 0
            self.packet_process_end = -1
        else:
            self.num_of_delay = self.num_of_delay + 1
            self.delay = self.delay + (self.time - self.queue[0])
            self.time_busy_server = self.time_busy_server + (self.time - self.prev_time)*self.server_status
            self.time_wait_in_queue = self.time_wait_in_queue + len(self.queue)*(self.time - self.prev_time)
            _, packet_length = self.generate_packet_mm1(bit_rate)
            self.packet_process_end = self.time + packet_length
            self.queue.pop(0)
    
    def update_clock(self):
        self.prev_time = self.time
        if (self.packet_arrival < self.packet_process_end) or (self.packet_process_end == -1):
            self.time = self.packet_arrival
            self.action_type = "A"
        else:
            self.time = self.packet_process_end
            self.action_type = "D"

    def start_mm1(self, simulation_time, bit_rate, processing_rate):
        self.init_action_lists(bit_rate)
        while(self.num_of_delay < simulation_time):
            self.update_clock()
            if (self.action_type == "A"):
                self.action_a_algorithm(bit_rate, processing_rate)
            elif (self.action_type == "D"):
                self.action_d_algorithm(bit_rate, processing_rate)
        print("number of packets: ", self.num_of_delay)
        print("mean delay for client: ", self.delay/self.num_of_delay)
        print("mean time in queue: ", self.time_wait_in_queue/self.num_of_delay)
        print("server busy: ", self.time_busy_server/self.time)
        # print( self.delay, self.time_busy_server, self.time_wait_in_queue, )

    def start_fifo(self, packet_length, bit_rate, num_of_sources):
        pass
        
    def start_prio(self):
        pass

#  speed: 300b/s 
#  deltaT: 5s
#  1500b -> 1 pakiet