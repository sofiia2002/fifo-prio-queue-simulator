from simulator import Simulator

def main():
    simulator = Simulator()
    # simulator.start_mm1(1000, 7, 8)
    #
    # simulation_time, bit_rate, service_rate
    simulator.start_fifo(3, 9000, 6000)

if __name__ == "__main__":
    main()