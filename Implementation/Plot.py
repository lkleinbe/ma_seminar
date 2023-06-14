


def figure_2(M=30, N=100, p=0.5):
    """backlog b_e vs violation probability e like in figure 2"""
    unreliability = 0
    sc = System_characteristics(M, N, 0)
    backlog_range = range(11)
    time = 50
    data = np.column_stack(simulation_violation_probabilty_over_backlog(sc, backlog_range, time, nr_of_instances))
    data = data[data[:, 0].argsort()]
    fig, ax = plt.subplots()
    ax.plot(data[:, 0], data[:, 1])
    plt.show()


def figure_3(M=10, t=range(100, 200, 100), list_range_nr_ues_start=None, b_e=0):
    """
    maximum number of supported UEs vs total burst resolution violation probability like in figure 3
    """
    if list_range_nr_ues_start is None:
        # list_range_nr_ues_start = [range(250, 750, 10), range(500, 1000, 10), range(750, 1250, 10)]
        list_range_nr_ues_start = [range(250, 750, 10)]
    fig, ax = plt.subplots()
    for t_instance, range_nr_ues_start in zip(t, list_range_nr_ues_start):
        print(f"t = {t_instance}")
        qos = QoS_requirement(b_e, t_instance, 0)
        data = np.column_stack(
            simulation_violation_probabilty_over_nr_ues_start(qos, M, range_nr_ues_start, nr_of_instances, AC_Mode.dynamic_barring))
        data = data[data[:, 0].argsort()]
        ax.plot(data[:, 1], data[:, 0], label=f"t= {t_instance}, sim")
    plt.xscale("log")
    plt.legend()
    plt.ylabel("max UEs supported")
    plt.xlabel("Violation probability")
    plt.grid()
    if save:
        plt.savefig('../Figures/figure_3.pgf')
    else:
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
    fig, ax = plt.subplots()
    for m in M:
        sc = System_characteristics(m, N, 0)
        data = np.column_stack(
            simulation_violation_probability_over_resolution_time(sc, b_e, time_range, nr_of_instances))
        data = data[data[:, 0].argsort()]
        ax.plot(data[:, 1], data[:, 0], label=f"m= {m}, sim")
    plt.show()

def figure_backlog(m = 20, N= 170):
    s1 = Simulation_instance(System_characteristics(m, N, 0), QoS_requirement(max_tolerated_backlog=0))
    s2 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.static_barring, 0.5),
                             QoS_requirement(max_tolerated_backlog=0))
    s3 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.dynamic_barring),
                             QoS_requirement(max_tolerated_backlog=0))
    s4 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.dynamic_estimated_barring),
                             QoS_requirement(max_tolerated_backlog=0))
    for x in s1:
        pass
    for x in s2:
        pass
    for x in s3:
        pass
    for x in s4:
        pass
    fig = plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(s1.backlog_over_time, label=f"{s1.sc.ac_mode}")
    plt.plot(s2.backlog_over_time, label=f"{s2.sc.ac_mode} p={s2.sc.ac_probability}")
    plt.plot(s3.backlog_over_time, label=f"{s3.sc.ac_mode}")
    plt.plot(s4.backlog_over_time, label=f"{s4.sc.ac_mode}")
    plt.ylabel("Backlog B")
    plt.xlabel("Time t")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    import matplotlib as mpl
    save = False
    if save:
        mpl.use("pgf")
        mpl.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
    import matplotlib.pyplot as plt
    from Simulation_violation_probability import *

    nr_of_instances = 10000
    # figure_3()
    figure_backlog()