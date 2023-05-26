from Backlog_deterministic_iterative import *
from math import *
from itertools import product


def mgf_max(o):
    m = sum([(((M ** x) * exp(-1 * M)) / (factorial(x))) * formel_3(k, x, M)]
            for (k, x) in prod(range(M), range(N)))
    # fixme what is M, n, t, O?
    return m


def formel_25(t2: int, b_e):
    m = min([exp(-b_e * o) * exp(o * N) * (mgf_max(o) ** t) + mgf_max(o) * (
                (1 - (mgf_max(o) ** (t - 1))) / (1 - mgf_max(o)))] for o in range(O))
    # fixme what is M, n, t, O?
    return m


def formel_4(b_i, B_i, p_i):
    """
    Implements formula (4) which specifies the number of admitted ues b_i with B(i) trials
    :param b_i: number of admitted Ues
    :param B_i: how many trials
    :param p_i: admission probability
    :return: the probability that the number of admitted ues is b_i
    """
    x = b_i
    n = B_i
    p = comb(n, x) * ((1 - p_i) ** x) * (p_i ** (n - x))
    return p


def formel_3(s_i, b_i, M):
    k = s_i
    x = b_i
    j_max = min(M - k, x - k)

    p = comb(x, k) * comb(M, k) * (factorial(k) / (M ** x))
    s = sum([(-1) ** j * comb(M - k, j) * comb(x - k, j) * factorial(j) * (M - k - j) ** (x - k - j)] for j in
            range(1, j_max, 1))
    return p * s


def formel_5(k, n, m, p_i):
    # fixme t2 missing?

    # alternatively we can use formula (21)
    return sum([formel_4(x, n, p_i) * formel_3(k, x, m)] for x in range(n))


def analysis(sc: System_characteristics, qos: QoS_requirement):
    results = []
    for x in range(qos.required_burst_resolution_time):
        # formel_25+formel_5
        p1 = 0
        p2 = 0
        results.append(p1 + p2)
    return sum(results)
