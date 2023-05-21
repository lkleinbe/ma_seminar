from Backlog_deterministic_iterative import *
import concurrent.futures


class Simulation_violation_probability:
    def __init__(self, sc: System_characteristics, qos: QoS_requirement, nr_of_instances: int):
        """
        Does a simulation with a given number of instances and evaluates violation probabilty
        :param sc:
        :param qos:
        :param nr_of_instances:
        """
        self.qos = qos
        self.sc = sc
        self.nr_of_instances = nr_of_instances
        self.simulations = [Simulation_instance(sc, qos) for _ in range(nr_of_instances)]

    def calculate_violation_probability(self):
        """
        Starts the Simulation
        :return: the found error unreliability
        """
        for simulation_instance in self.simulations:
            for _ in simulation_instance:
                pass
        return sum([not iterator.success for iterator in self.simulations]) / self.nr_of_instances


def simulation_violation_probabilty_worker(sc: System_characteristics, qos: QoS_requirement, nr_of_instances: int):
    """
    worker function for the worker threads. Wraps the Simulation_violation_probabilty Class
    :param sc: The given System characteristics
    :param qos: The given Quality of Service requirements
    :param nr_of_instances: How many instances should the simulation have
    :return: The found violation probability
    """
    s = Simulation_violation_probability(sc, qos, nr_of_instances)
    return s.calculate_violation_probability()


def simulation_violation_probabilty_over_nr_ues_start(qos: QoS_requirement, nr_channels: int, range_nr_ues_start: range,
                                                      nr_of_instances: int):
    """
    Does a simulation over a range of ues and returns the violation probabilites
    :param qos: The given QoS_requirement that has to be fullfilled
    :param nr_channels: the given number of channels. will be used to construct a System characteristic with range_nr_ues_start
    :param range_nr_ues_start: the range over which nr_ues_start should be varied
    :param nr_of_instances: how many instances should each simulation have
    :return: a list with the violation probabilities
    """
    nr_ues_start_return = []
    violation_probability_return = []
    futures_to_arguments = {}
    scs = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for nr_ues_start in range_nr_ues_start:
            scs.append(System_characteristics(20, nr_ues_start, 0))
        for sc_i in range(len(scs)):
            futures_to_arguments[executor.submit(
                simulation_violation_probabilty_worker, scs[sc_i], qos, nr_of_instances)] = scs[sc_i]
        for future in concurrent.futures.as_completed(futures_to_arguments):
            # print(f"{futures_to_arguments[future]}: {future.result()}")
            nr_ues_start_return.append(futures_to_arguments[future].nr_ues_start)
            violation_probability_return.append(future.result())
    return nr_ues_start_return, violation_probability_return


def simulation_violation_probabilty_over_backlog(sc: System_characteristics, backlog_range: range,
                                                 required_burst_resolution_time: int, unreliability: float = 0):
    """
    Does a simulation over a range of maximum tolerated backlogs. Time is fixed
    :param unreliability: the allowed unreliability
    :param sc: The given System_characteristics
    :param backlog_range: the range over which the backlog should vary
    :param required_burst_resolution_time: the required_burst_resolution time
    :return: a list with the violation probabilities
    """
    backlog_return = []
    violation_probability_return = []
    futures_to_arguments = {}
    qoss = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for backlog in backlog_range:
            qoss.append(QoS_requirement(backlog, required_burst_resolution_time, unreliability))
        for qos_i in range(len(qoss)):
            futures_to_arguments[executor.submit(
                simulation_violation_probabilty_worker, sc, qoss[qos_i], nr_of_instances)] = qoss[qos_i]
        for future in concurrent.futures.as_completed(futures_to_arguments):
            print(f"{futures_to_arguments[future]}: {future.result()}")
            backlog_return.append(futures_to_arguments[future].max_tolerated_backlog)
            violation_probability_return.append(future.result())
    return backlog_return, violation_probability_return


def simulation_violation_probability_over_resolution_time(sc: System_characteristics, max_tolerated_backlog: int,
                                                          required_burst_resolution_time_range: range,
                                                          unreliability: float = 0):
    time_return = []
    violation_probability_return = []
    futures_to_arguments = {}
    qoss = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for required_burst_resolution_time in required_burst_resolution_time_range:
            qoss.append(QoS_requirement(max_tolerated_backlog, required_burst_resolution_time, 0))
        for qos_i in range(len(qoss)):
            futures_to_arguments[executor.submit(
                simulation_violation_probabilty_worker, sc, qoss[qos_i], nr_of_instances)] = qoss[qos_i]
        for future in concurrent.futures.as_completed(futures_to_arguments):
            print(f"{futures_to_arguments[future]}: {future.result()}")
            time_return.append(futures_to_arguments[future].required_burst_resolution_time)
            violation_probability_return.append(future.result())
        return violation_probability_return, violation_probability_return


if __name__ == "__main__":
    # s = Simulation_violation_probability(System_characteristics(20, 160, 0),
    #                                      QoS_requirement(required_burst_resolution_time=500), 1000)
    # print(s.calculate_violation_probability())
    #
    # qos = QoS_requirement(required_burst_resolution_time=500)
    # sc = System_characteristics(20, 160, 0)
    #
    # print(simulation_violation_probabilty_worker(sc, qos, 1000))

    # qos = QoS_requirement(required_burst_resolution_time=500)
    # channel = 20
    # range_nr_ues_start = range(10, 300, 10)
    # nr_of_instances = 1000
    # print(list(zip(*simulation_violation_probabilty_over_nr_ues_start(qos, channel, range_nr_ues_start, nr_of_instances))))

    required_burst_resolution_time: int
    sc = System_characteristics(20, 180, 0)
    range_backlog = range(10, 500, 10)
    nr_of_instances = 1000
    # simulation_violation_probabilty_over_backlog(sc, range_backlog, 500)
    range_time = range(200, 700, 10)
    simulation_violation_probability_over_resolution_time(sc, 150, range_time)
