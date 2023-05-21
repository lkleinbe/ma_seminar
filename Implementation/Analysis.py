from Backlog_deterministic_iterative import *


def formel_25(t2: int):
    # todo implement (25)
    pass


def formel_4(b_i, B_i):
    # todo implement
    pass


def formel_3(s_i, b_i):
    # todo implement
    pass


def formel_5(t1):
    # todo implement(5)
    pass


def analysis(sc: System_characteristics, qos: QoS_requirement):
    results = []
    for x in range(qos.required_burst_resolution_time):
        # formel_25+formel_5
        p1 = 0
        p2 = 0
        results.append(p1 + p2)
    return sum(results)
