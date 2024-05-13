# prunign and sharing based optimization
from math import log, pi


# n is len(v1)
#
def calc_running_confidence_interval(m, n, d):
    x = (1 - (m - 1) / n) * 2 * log(log(m)) + log(pi**2 / 3 * d)
    return (x / (2 * m)) ** 0.5


def calc_bounds(m, query_obj, delta):
    query_dict = {}
    for k, v in query_obj.items():
        avg = sum(v) / len(v)
        query_dict[k]["avg"] = avg
        ci = calc_running_confidence_interval(m, len(query_obj[k]), delta)
        query_dict[k]["upper"] = avg + ci
        query_dict[k]["lower"] = avg - ci

    return query_dict


# split dataset #every split call calc_running ...

# every tuple amf kl-divergence (utility fx)
# some tuple amf (if low) get rid of it

# some tuple amf-amf_1
