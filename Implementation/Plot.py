import matplotlib.pyplot as plt

from Simulation_violation_probability import *


def figure_2(M=30, N=100, p=0.5):
    """backlog b_e vs violation probability e like in figure 2"""
    unreliability = 0;
    sc = System_characteristics(M, N, 0)
    backlog_range = range(11)
    time = 50
    # there got to be a better way to do this. maybe stack directly
    # data = np.array(list(zip(*simulation_violation_probabilty_over_backlog(sc, backlog_range, time, 10000))))
    data = np.column_stack(simulation_violation_probabilty_over_backlog(sc, backlog_range, time, nr_of_instances))
    data = data[data[:, 0].argsort()]
    fig, ax = plt.subplots()
    ax.plot(data[:, 0], data[:, 1])
    plt.show()


def figure_3(M=10, t=range(100, 400, 100), b_e=0):
    """
    maximum number of supported UEs vs total burst resolution violation probability like in figure 3
    """
    range_nr_ues_start = range(200, 1600, 100)
    fig, ax = plt.subplots()
    for t_instance in t:
        qos = QoS_requirement(b_e, t_instance, 0)
        data = np.column_stack(
            simulation_violation_probabilty_over_nr_ues_start(qos, M, range_nr_ues_start, nr_of_instances))
        data = data[data[:, 0].argsort()]
        ax.plot(data[:, 1], data[:, 0], label=f"t= {t_instance}, sim")
    plt.show()


def figure_4(M=range(10, 30, 10), N=1000):
    """
    burst resolution time vs partial violation probability like in Fig 4
    """
    time_range = range(0, 360, 10)
    fig, ax = plt.subplots()
    for m in M:
        sc = System_characteristics(m, N, 0)
        b_e = 3 * m
        data = np.column_stack(
            simulation_violation_probability_over_resolution_time(sc, b_e, time_range, nr_of_instances))
        data = data[data[:, 0].argsort()]
        ax.plot(data[:, 1], data[:, 0], label=f"m= {m}, sim")
    plt.show()

def figure_5(M=range(10, 30, 10), N=1000):
    """
    burst resolution time vs violation probability like in Fig 5
    """
    time_range = range(0, 360, 10)
    b_e = 0

    for m in M:
        sc = System_characteristics(m, N, 0)
        data = np.column_stack(
            simulation_violation_probability_over_resolution_time(sc, b_e, time_range, nr_of_instances))
        data = data[data[:, 0].argsort()]
        ax.plot(data[:, 1], data[:, 0], label=f"m= {m}, sim")
    plt.show()

if __name__ == "__main__":
    nr_of_instances = 10000
    figure_4()
