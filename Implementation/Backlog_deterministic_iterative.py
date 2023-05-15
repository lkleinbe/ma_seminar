import numpy as np
import operator
import timeit
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class QoS_requirement:
    """
    Contains the QoS_requirements
    :var max_tolerated_backlog: The maximum support backlog b^epsilon
    :var required_burst_resolution_time: the time by which we have to be done t
    :var unreliability: the probability that a burst is not resolved by t
    """
    max_tolerated_backlog: int = 0
    required_burst_resolution_time: float = float("inf")
    unreliability: float = 0.0


@dataclass
class System_characteristics:
    """
    Contains the System characteristics.
    :var max_channels: how many channels
    :var nr_ues_start: how many ues at the start of the simulation
    :var nr_ues_new: how many ues are added per timestep
    """
    max_channels: int
    nr_ues_start: int
    nr_ues_new: int


class Simulation_instance(object):
    def __init__(self, sc: System_characteristics, qos: QoS_requirement):
        """
        One Instance of a simulation implemented as a generator
        :param sc: The given System Characteristics
        :param qos: the qos_requirement we are checking
        """
        self.sc = sc
        self.qos = qos

        self.t_current = 0
        self.backlog_current = sc.nr_ues_start
        self.backlog_over_time = [self.backlog_current]
        self.success = False

    def __iter__(self):
        return self

    def __next__(self):
        """one simulation step aka one subframe"""
        self.t_current += 1
        active_ues = self.backlog_current + self.sc.nr_ues_new
        selected_channels = np.random.randint(0, self.sc.max_channels, active_ues)
        counts = np.bincount(selected_channels)
        s_i = operator.countOf(counts, 1)
        self.backlog_current = active_ues - s_i
        self.backlog_over_time.append(self.backlog_current)
        if self.backlog_current <= self.qos.max_tolerated_backlog:
            self.success = True
            raise StopIteration()
        elif self.t_current >= self.qos.required_burst_resolution_time:
            raise StopIteration()
        else:
            return self.backlog_current


if __name__ == "__main__":
    s = Simulation_instance(System_characteristics(20, 160, 0), QoS_requirement(required_burst_resolution_time=500))
    for x in s:
        print(x)
    plt.plot(s.backlog_over_time)
    plt.show()
    # print(timeit.timeit(
    #     "for _ in Simulation_instance(System_characteristics(20, 160, 0), QoS_requirement(required_burst_resolution_time=500)): pass",
    #     globals=globals(), number=1000))
