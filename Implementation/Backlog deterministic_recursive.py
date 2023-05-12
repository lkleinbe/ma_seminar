import random
import collections
import numpy as np
import operator
import timeit

a_i = 0  # newly activated UEs
m = 20  # nr_of_channels

nr_ues = 180
nr_ues_new = 0


# Not used because slow

# def calc_si_Counter(selected_channels):
#     nr_of_selections = collections.Counter(selected_channels)
#     s_i = operator.countOf(nr_of_selections.values(), 1)
#     return s_i
#
#
# def calc_si_npunique(selected_channels):
#     _, counts = np.unique(selected_channels, return_counts=True)
#     # print(counts)
#     s_i = operator.countOf(counts, 1)
#     return s_i


def calc_si_bincount_countof(selected_channels):
    counts = np.bincount(selected_channels)
    s_i = operator.countOf(counts, 1)
    return s_i


def calc_si_bincount_selection(selected_channels):
    counts = np.bincount(selected_channels)
    s_i = sum(counts[counts == 1])
    # print(counts, s_i)
    return s_i


# Not used because slow

# def backlog_determistic_Counter(t):
#     if t == 0:
#         return nr_ues
#     else:
#         active_ues = backlog_determistic_Counter(t - 1) + nr_ues_new
#         selected_channels = np.random.randint(0, m, active_ues)
#         s_i = calc_si_Counter(selected_channels)
#         return active_ues - s_i
#
#
# def backlog_determistic_unique(t):
#     if t == 0:
#         return nr_ues
#     else:
#         active_ues = backlog_determistic_unique(t - 1) + nr_ues_new
#         selected_channels = np.random.randint(0, m, active_ues)
#         s_i = calc_si_npunique(selected_channels)
#         return active_ues - s_i


def backlog_deterministic_bincount_countof(t):
    if t == 0:
        return nr_ues
    else:
        active_ues = backlog_deterministic_bincount_countof(t - 1) + nr_ues_new
        selected_channels = np.random.randint(0, m, active_ues)
        s_i = calc_si_bincount_countof(selected_channels)
        return active_ues - s_i


def backlog_deterministic_bincount_selection(t):
    if t == 0:
        return nr_ues
    else:
        active_ues = backlog_deterministic_bincount_selection(t - 1) + nr_ues_new
        selected_channels = np.random.randint(0, m, active_ues)
        s_i = calc_si_bincount_selection(selected_channels)
        return active_ues - s_i


if __name__ == "__main__":
    # backlog_determistic_Counter(100)
    # backlog_determistic_unique(100)
    # backlog_deterministic_bincount_countof(100)
    n = 1000
    t_max = 500
    # print(timeit.timeit(f"backlog_determistic_Counter({t_max})", globals=globals(), number=n))
    # print(timeit.timeit(f"backlog_determistic_unique({t_max})", globals=globals(), number=n))

    # print(backlog_deterministic_bincount_selection(t_max))
    print(timeit.timeit(f"backlog_deterministic_bincount_countof({t_max})", globals=globals(), number=n))
    print(timeit.timeit(f"backlog_deterministic_bincount_selection({t_max})", globals=globals(), number=n))