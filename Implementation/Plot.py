from Simulation_violation_probability import *
import matplotlib.pyplot as plt
import timeit
def figure_2(save, M=30, N=100, p=0.5, nr_of_instances= 100_000):
    """backlog b_e vs violation probability e like in figure 2"""

    sc = System_characteristics(M, N, 0, AC_Mode.static_barring, p)
    backlog_range = range(11)
    time = 15
    data = np.column_stack(simulation_violation_probabilty_over_backlog(sc, backlog_range, time, nr_of_instances))
    data = data[data[:, 0].argsort()]
    fig, ax = plt.subplots()
    ax.plot(data[:, 0], data[:, 1])
    plt.yscale("log")
    plt.grid()

    # plt.xticks(range(11))
    plt.xlabel("Backlog")
    plt.ylabel("Violation prob.")
    ax.set_ylim(ymax=1, ymin = 1e-5)
    if save:
        plt.savefig('../Figures/figure_2.pgf')
    else:
        plt.title(f"violation Probability vs. Backlog\n $M = {M}$, $N = {N}$,$t = {time}$, static ACB $p={p}$")
        plt.show()


def figure_3(save, M=10, t=range(100, 400, 100), list_range_nr_ues_start=None, b_e=0, nr_of_instances = 10000):
    """
    maximum number of supported UEs vs total burst resolution violation probability like in figure 3
    """
    if list_range_nr_ues_start is None:
        list_range_nr_ues_start = [range(250, 750, 10), range(500, 1000, 10), range(750, 1250, 10)]
        # list_range_nr_ues_start = [range(250, 750, 10)]
    fig, ax = plt.subplots()
    for t_instance, range_nr_ues_start in zip(t, list_range_nr_ues_start):
        print(f"t = {t_instance}")
        qos = QoS_requirement(b_e, t_instance, 0)
        data = np.column_stack(
            simulation_violation_probabilty_over_nr_ues_start(qos, M, range_nr_ues_start, nr_of_instances, AC_Mode.optimal_dynamic_barring))
        data = data[data[:, 0].argsort()]
        ax.plot(data[:, 1], data[:, 0], label=f"$t= {t_instance}$, sim")
    plt.xscale("log")
    plt.legend()
    plt.ylabel("max UEs supported")
    plt.xlabel("Violation probability")
    plt.grid()
    if save:
        plt.savefig('../Figures/figure_3.pgf')
    else:
        plt.title(f"maximum number of supported UEs vs total burst resolution violation probability for $M = {M}$")
        plt.show()


def figure_4(save, M=range(10, 30, 10), N=1000):
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
        ax.plot(data[:, 1], data[:, 0], label=f"$m= {m}$, sim")
    if save:
        plt.savefig('../Figures/figure_4.pgf')
    else:
        plt.title(f"burst resolution time vs partial violation probability, $N = {N}$")
        plt.show()

def figure_5(save, M=range(10, 30, 10), N=1000, nr_of_instances= 10_000):
    """
    violation probability vs Burst resolution time like in Fig 5
    """
    time_ranges = [range(200, 400, 2), range(0, 200, 2)]
    # time_range = range(0, 360, 10)
    b_e = 0
    fig, ax = plt.subplots()
    for m, time_range in zip(M, time_ranges):
        sc1 = System_characteristics(m, N, 0, AC_Mode.optimal_dynamic_barring)
        data1 = np.column_stack(
            simulation_violation_probability_over_resolution_time(sc1, b_e, time_range, nr_of_instances))
        print(data1)
        data1 = data1[data1[:, 0].argsort()]
        # print(data1)
        ax.plot(data1[:, 0], data1[:, 1], label=f"m= {m}, sim")
        sc2 = System_characteristics(m, N, 0, AC_Mode.estimated_dynamic_barring)
        data2 = np.column_stack(
            simulation_violation_probability_over_resolution_time(sc2, b_e, time_range, nr_of_instances))
        data2 = data2[data2[:, 0].argsort()]
        ax.plot(data2[:, 0], data2[:, 1], label=f"$m= {m}$, sim (est)")
    plt.yscale("log")
    plt.grid()
    plt.legend()
    # plt.xticks(range(11))
    plt.xlabel("Burst resolution time t slots")
    plt.ylabel("Violation probability.")
    if save:
        plt.savefig('../Figures/figure_5.pgf')
    else:
        plt.title(f"burst resolution time vs violation probability, $N = {N}$")
        plt.show()

def figure_backlog(save, m = 20, N= 170):
    """
    Backlog vs time
    """
    s1 = Simulation_instance(System_characteristics(m, N, 0), QoS_requirement(max_tolerated_backlog=0))
    s2 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.static_barring, 0.5),
                             QoS_requirement(max_tolerated_backlog=0))
    s3 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.optimal_dynamic_barring),
                             QoS_requirement(max_tolerated_backlog=0))
    s4 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.estimated_dynamic_barring),
                             QoS_requirement(max_tolerated_backlog=0))
    for x in s1:
        pass
    for x in s2:
        pass
    for x in s3:
        pass
    for x in s4:
        pass
    fig = plt.figure() # figsize=(4, 3), dpi=80
    plt.plot(s1.backlog_over_time, label=f"No ACB")
    plt.plot(s2.backlog_over_time, label=f"Static ACB,  $p={s2.sc.ac_probability}$")
    plt.plot(s3.backlog_over_time, label=f"Optimal ACB")
    plt.plot(s4.backlog_over_time, label=f"Estimated Dynamic ACB")
    plt.ylabel("Backlog B")
    plt.xlabel("Time t")
    plt.grid()
    plt.legend()
    if save:
        plt.savefig('../Figures/figure_backlog.pgf')
    else:
        plt.title(f"Backlog over Time for different ACB, $m = {m}$, $N = {N}$")
        plt.show()

def figure_backlog_withACB(save, m = 20, N= 170):
    """
    Backlog vs time
    """
    # s1 = Simulation_instance(System_characteristics(m, N, 0), QoS_requirement(max_tolerated_backlog=0))
    s2 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.static_barring, 0.5),
                             QoS_requirement(max_tolerated_backlog=0))
    s3 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.optimal_dynamic_barring),
                             QoS_requirement(max_tolerated_backlog=0))
    s4 = Simulation_instance(System_characteristics(m, N, 0, AC_Mode.estimated_dynamic_barring),
                             QoS_requirement(max_tolerated_backlog=0))
    # for x in s1:
    #     pass
    for x in s2:
        pass
    for x in s3:
        pass
    for x in s4:
        pass
    fig = plt.figure() # figsize=(4, 3), dpi=80
    # plt.plot(s1.backlog_over_time, label=f"No ACB")
    plt.plot(s2.backlog_over_time, label=f"Static ACB,  $p={s2.sc.ac_probability}$")
    plt.plot(s3.backlog_over_time, label=f"Optimal ACB")
    plt.plot(s4.backlog_over_time, label=f"Estimated Dynamic ACB")
    plt.ylabel("Backlog B")
    plt.xlabel("Time t")
    plt.grid()
    plt.legend()
    if save:
        plt.savefig('../Figures/figure_backlog.pgf')
    else:
        plt.title(f"Backlog over Time for different ACB, $m = {m}$, $N = {N}$")
        plt.show()



def figure_runtime(save, m = 20, N = 170):
    """
    Run Time vs ACB Policy
    """
    runtime_no_barring = timeit.timeit(
        f"for _ in Simulation_instance(System_characteristics({m}, {N}, 0, AC_Mode.no_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000)

    runtime_static_barring = timeit.timeit(
        f"for _ in Simulation_instance(System_characteristics({m}, {N}, 0, AC_Mode.static_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000)

    runtime_optimal_barring = timeit.timeit(
        f"for _ in Simulation_instance(System_characteristics({m}, {N}, 0, AC_Mode.optimal_dynamic_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000)




    runtime_estimated_barring= timeit.timeit(
        f"for _ in Simulation_instance(System_characteristics({m}, {N}, 0, AC_Mode.estimated_dynamic_barring, 0.5), QoS_requirement(required_burst_resolution_time=500)): pass",
        globals=globals(), number=10000)

    plt.bar(["No Barring", "Static $p = 0.5$", "Optimal ", "Estimated "], [runtime_no_barring/10000, runtime_static_barring/10000, runtime_optimal_barring/10000, runtime_estimated_barring/10000])
    plt.ylabel("Time in s")

    plt.grid()
    if save:
        plt.savefig('../Figures/figure_runtime.pgf')
    else:
        plt.title(f"Run Time vs ACB, $m = {m}$, $N = {N}$")
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


    nr_of_instances = 10000
    # figure_2()
    # figure_backlog()
    # figure_runtime()