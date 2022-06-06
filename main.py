from simulator_fifo import SimulatorFifo
from simulator_prio import SimulatorPrio
import matplotlib.pyplot as plt
import numpy as np

def main():
    simulator = SimulatorFifo()
    simulator_2 = SimulatorPrio([2, 1])
    # simulation_time, bit_rate, service_rate
    delay, time_wait_in_queue, _, _ = simulator.start_fifo(10, 1000, [3000, 3000], [1000, 1000], 6000)
    delay1, time_wait_in_queue1, _, _ = simulator_2.start_fifo(10, 1000, [3000, 3000], [1000, 1000], 6000)

    plt.boxplot(delay)
    plt.title("Delay for FIFO")
    plt.show()

    plt.boxplot(time_wait_in_queue)
    plt.title("Clients in queue for FIFO")
    plt.show()

    plt.boxplot(delay1)
    plt.title("Delay for PRIO")
    plt.show()

    plt.boxplot(time_wait_in_queue1)
    plt.show()

if __name__ == "__main__":
    main()