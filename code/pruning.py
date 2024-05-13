# prunign and sharing based optimization
from math import log, pi


# n is len(v1)
#
def calc_running_confidence_interval(m, n, d):
    x = (1 - (m - 1) / n) * 2 * log(log(m)) + log(pi**2 / 3 * d)
    return (x / (2 * m)) ** 0.5


# N and delta are assigned outside of the method
def calc_bounds(query_obj, N, delta):
    query_dict = {}
    for k, v in query_obj.items():
        avg = sum(v) / len(v)
        query_dict[k]["avg"] = avg
        ci = calc_running_confidence_interval(len(query_obj[k]), N, delta)
        query_dict[k]["upper"] = avg + ci
        query_dict[k]["lower"] = avg - ci

    return query_dict


# split dataset #every split call calc_running ...

# every tuple amf kl-divergence (utility fx)
# some tuple amf (if low) get rid of it

# some tuple amf-amf_1

def prune_based_on_confidence_intervals(queries, delta):
    # Calculate confidence intervals for each query
    bounds = calc_bounds(len(queries), queries, delta)
    
    # Sort queries by upper bound of confidence interval
    sorted_queries = sorted(bounds.items(), key=lambda x: x[1]["upper"])
    
    # Find the lowest lower bound among the top queries
    top_queries = sorted_queries[:5] 
    lowest_lower_bound = min(query[1]["lower"] for query in top_queries)
    
    # Prune queries with upper bound lower than lowest lower bound
    pruned_queries = []
    for query in top_queries:
        if query[1]["upper"] < lowest_lower_bound:
            pruned_queries.append(query[0])

    return pruned_queries