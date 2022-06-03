from simulator_fifo import Simulator

def main():
    simulator = Simulator()
    # simulation_time, bit_rate, service_rate
    simulator.start_fifo(3, [5000, 5000], [1000, 1000], 6000)

if __name__ == "__main__":
    main()