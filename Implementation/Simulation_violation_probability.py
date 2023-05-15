from Backlog_deterministic_iterative import *


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


if __name__ == "__main__":
    s = Simulation_violation_probability(System_characteristics(20, 160, 0),
                                         QoS_requirement(required_burst_resolution_time=500), 1000)
    print(s.calculate_violation_probability())
