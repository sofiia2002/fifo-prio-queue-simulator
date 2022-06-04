from simulator_fifo import SimulatorFifo
from simulator_prio import SimulatorPrio

def main():
    # simulator = SimulatorFifo()
    simulator_2 = SimulatorPrio([2, 1])
    # simulation_time, bit_rate, service_rate
    # simulator.start_fifo(3, [5000, 5000], [1000, 1000], 6000)
    simulator_2.start_fifo(3, [5000, 6000], [1000, 1000], 6000)

if __name__ == "__main__":
    main()