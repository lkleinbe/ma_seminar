import numpy as np
import operator
import timeit
import matplotlib.pyplot as plt


class Simulation(object):
    def __init__(self, t_max, nr_ues_start, nr_ues_new, max_channels):
        self.max_channels = max_channels
        self.nr_ues_new = nr_ues_new
        self.nr_ues_start = nr_ues_start
        self.t_max = t_max
        self.t_current = 0
        self.backlog_current = nr_ues_start
        self.backlog_over_time = [self.backlog_current]

    def __iter__(self):
        return self

    def __next__(self):
        self.t_current += 1
        if self.t_current >= self.t_max:
            raise StopIteration
        active_ues = self.backlog_current + self.nr_ues_new
        selected_channels = np.random.randint(0, self.max_channels, active_ues)
        counts = np.bincount(selected_channels)
        s_i = operator.countOf(counts, 1)
        self.backlog_current = active_ues - s_i
        self.backlog_over_time.append(self.backlog_current)
        if self.backlog_current:
            return self.backlog_current
        else:
            raise StopIteration()


if __name__ == "__main__":
    s = Simulation(500, 160, 0, 20)
    for x in s:
        print(x)
    plt.plot(s.backlog_over_time)
    plt.show()
    print(timeit.timeit("for _ in Simulation(500, 180, 0, 20): pass", globals=globals(), number=1000))

