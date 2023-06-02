"""
Simulation of 1 instance in an iterative way. Executing this plots the backlog and does a performance test.
The performance test is impacted by the number of executed steps. dynamic barring does need less steps and is
therefore faster
"""
import numpy as np
import operator
import timeit
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum, auto
from math import ceil


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


class AC_Mode(Enum):
    """
    Different access barring modes available. For static_barring the ac_probability field in
     System characteristics is used
    """
    no_barring = auto()
    static_barring = auto()
    dynamic_barring = auto()
    dynamic_estimated_barring = auto()


@dataclass
class System_characteristics:
    """
    Contains the System characteristics.
    :var max_channels: how many channels
    :var nr_ues_start: how many ues at the start of the simulation
    :var nr_ues_new: how many ues are added per timestep
    :var ac_mode: which access barring mode to use. default is no barring
    :var ac_probability: which access barring probability to use. only works with access barring
    """
    max_channels: int
    nr_ues_start: int
    nr_ues_new: int
    ac_mode: AC_Mode = AC_Mode.no_barring
    ac_probability: float = 1.0






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

        # Parameters dynamic estimated access barring
        self.s_i= None
        self.v = self.sc.max_channels
        self.p = 1/self.sc.max_channels

        def contention(active_ues):
            """
            Calculates one conention phase aka one subframe. will raise StopIteration if the simulation is finished
            :param active_ues: The given number of ues to participate in the contention
            :return: the current backlog.
            """
            selected_channels = np.random.randint(0, self.sc.max_channels, active_ues)
            counts = np.bincount(selected_channels)
            self.s_i = operator.countOf(counts, 1)
            self.backlog_current -= self.s_i
            self.backlog_over_time.append(self.backlog_current)
            if self.backlog_current <= self.qos.max_tolerated_backlog:
                self.success = True
                raise StopIteration()
            elif self.t_current >= self.qos.required_burst_resolution_time:
                raise StopIteration()
            else:
                return self.backlog_current

        def func_no_barring(_):
            """
            One Simulation step for no access baring. Is equal to static barring with ac_probability==1 but
            we don't have to perform the operation
            :return: the current backlog
            """
            self.t_current += 1
            self.backlog_current += self.sc.nr_ues_new
            active_ues = self.backlog_current
            return contention(active_ues)


        def func_static_barring(_):
            """
            One Simulation step for static access baring.
            :return: the current backlog
            """
            self.t_current += 1
            self.backlog_current += self.sc.nr_ues_new
            active_ues = np.random.binomial(self.backlog_current, self.sc.ac_probability)
            return contention(active_ues)

        def func_dynamic_barring(_):
            """
            One Simulation step for dynamic access baring with optimal barring
            :return: the current backlog
            """
            self.t_current += 1
            self.backlog_current += self.sc.nr_ues_new
            p= min(1.0, self.sc.max_channels / self.backlog_current) # optimal access barring policy as in (7)
            active_ues = np.random.binomial(self.backlog_current, p)
            return contention(active_ues)

        def func_dynamic_estimated_barring(_):
            """
            One Simulation step for dynamic access baring but with estimated probability.
            :return: the current backlog
            """
            self.t_current += 1
            self.backlog_current += self.sc.nr_ues_new
            active_ues = np.random.binomial(self.backlog_current, self.p)
            backlog_current = contention(active_ues)

            # for next step
            delta_v = (0.582 * self.sc.max_channels) - 1.582 * (self.sc.max_channels-self.s_i)
            self.v += delta_v
            a_t = max(0, delta_v)
            self.v += a_t - self.s_i    # c_t = self.s_i
            self.v = max(self.sc.max_channels, self.v)
            self.p = min(1.0, self.sc.max_channels/self.v)
            return backlog_current

        if self.sc.ac_mode == AC_Mode.no_barring:  # don't do this at home
            self.functionnext = func_no_barring
        elif self.sc.ac_mode == AC_Mode.static_barring:
            self.functionnext = func_static_barring
        elif self.sc.ac_mode == AC_Mode.dynamic_barring:
            self.functionnext = func_dynamic_barring
        elif self.sc.ac_mode == AC_Mode.dynamic_estimated_barring:
            self.functionnext = func_dynamic_estimated_barring


    def __next__(self):
        """
        One Simulation step
        :return: the current backlog
        """
        return self.functionnext(self)  # this is an evil hack. because I added access barring after the simulation but
    # don't want to test every time i run this function. what we do for performance...

    def __iter__(self):
        return self


if __name__ == "__main__":
    s1 = Simulation_instance(System_characteristics(20, 170, 0), QoS_requirement(max_tolerated_backlog=0))
    s2 = Simulation_instance(System_characteristics(20, 170, 0, AC_Mode.static_barring, 0.5), QoS_requirement(max_tolerated_backlog=0))
    s3 = Simulation_instance(System_characteristics(20, 170, 0, AC_Mode.dynamic_barring), QoS_requirement(max_tolerated_backlog=0))
    s4 = Simulation_instance(System_characteristics(20,170,0, AC_Mode.dynamic_estimated_barring), QoS_requirement(max_tolerated_backlog=0))
    print("Backlog no barring")
    for x in s1:
        print(x)
    print("Backlog static barring")
    for x in s2:
        print(x)
    print("Backlog dynamic barring")
    for x in s3:
        print(x)
    print("Backlog dynamic estimated barring")
    for x in s4:
        print(x)
    fig = plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(s1.backlog_over_time, label = f"{s1.sc.ac_mode}")
    plt.plot(s2.backlog_over_time, label = f"{s2.sc.ac_mode} p={s2.sc.ac_probability}")
    plt.plot(s3.backlog_over_time, label = f"{s3.sc.ac_mode}")
    plt.plot(s4.backlog_over_time, label=f"{s4.sc.ac_mode}")
    plt.yscale("log")
    plt.legend(bbox_to_anchor=(0.5, -0.015), loc="lower center",
                bbox_transform=fig.transFigure, ncol=2,mode="expand")
    # fig.legend(loc=7)
    # fig.tight_layout()
    # fig.subplots_adjust(right=0.75)
    plt.show()
    print("No Barring execution Time: ", timeit.timeit(
        "for _ in Simulation_instance(System_characteristics(20, 170, 0, AC_Mode.no_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000))
    print("Static Barring execution Time: ", timeit.timeit(
        "for _ in Simulation_instance(System_characteristics(20, 170, 0, AC_Mode.static_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000))
    print("Dynamic Barring execution Time: ", timeit.timeit(
        "for _ in Simulation_instance(System_characteristics(20, 170, 0, AC_Mode.dynamic_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000))
    print("Dynamic Estimated Barring execution Time: ", timeit.timeit(
        "for _ in Simulation_instance(System_characteristics(20, 170, 0, AC_Mode.dynamic_estimated_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000))
