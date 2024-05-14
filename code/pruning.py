import numpy as np
import pandas as pd
import psycopg2
import scipy
from math import log
from math import pi
import sys
import time




start_time = time.time()
conn = psycopg2.connect(database="census", user="", password="", host="localhost",port="5432")


# includes married people
D_Q = "married"

# includes unmarried people
D_R = "unmarried"

D = [D_Q, D_R]

# dimension attribute (for group by)
A = ['workclass', 'education', 'occupation', 'relationship', 'race', 'sex', 'native_country', 'income']
# Measure attribute (for aggregate)
M = ['age', 'fnlwgt', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week']
# aggregate function
F = ['MIN', 'MAX', 'COUNT', 'SUM', 'AVG']


'''
obj query_obj = {a: element in A, m: element in M, f: element in F, d: database name, 
query: sql query, query_res: result list of tuples} query_res example: [('china', f(m)), ('US', f(m))] list of numbers between 0 and 1
'''


# iterate a, m, f into this query
# SELECT a, f(m), FROM D group by a
def generate_queries(A, M, F, D):
    query_obj = {}
    cur = conn.cursor()
    for a in A:
        for m in M:
            for f in F:
                for d in D:
                    query = f"SELECT {a}, {f}({m}) FROM {d} WHERE {a} IS NOT NULL GROUP BY {a}"
                    cur.execute(query)
                    conn.commit()
                    query_obj[(a, m, f, d)] = cur.fetchall()
    conn.close()
    return query_obj


def normalization(arr1, arr2):
    sum1 = sum(arr1)
    sum2 = sum(arr2)
    norm_1 = [elem / sum1 for elem in arr1]
    norm_2 = [elem / sum2 for elem in arr2]
    return norm_1, norm_2


# This function outputs the two normalized arrays for a specific a, m, f query with married and unmarried
def get_normalized_list(query_obj1, query_obj2):
    arr1 = []
    arr2 = []

    # converting the tuples into dictionary for easier manipulation
    query_tuple_dict_1 = dict(query_obj1)
    query_tuple_dict_2 = dict(query_obj2)

    # find common attributes of the keys for evaluation
    common_attribute = set(query_tuple_dict_1.keys()) & set(query_tuple_dict_2.keys())
    # appending into the list, uses 1e-10 to avoid the scipy.stats.entropy warning
    for key in common_attribute:
        num1 = float(query_tuple_dict_1[key])
        num2 = float(query_tuple_dict_2[key])
        arr1.append(float(num1) if num1 != 0 else float(1e-10))
        arr2.append(float(num2) if num2 != 0 else float(1e-10))

    return normalization(arr1, arr2)

def calc_running_confidence_interval(m, n, d):
    x = (1 - (m - 1) / n) * 2 * log(log(m)) + log(pi**2 / 3 * d)
    return (x / (2 * m)) ** 0.5

# queryobj[(a,m,f,d)] = query result: list of tuples
def get_res(query_obj):
    # result_dict[(a,m,f)] = distance
    result_dict = {}
    partition_size = 0
    prune_set = set()
    # k = (a,m,f,d) v = [query, queryres]
    for k, v in query_obj.items():
        result_k = k[:-1]
        if result_k in result_dict:
            continue
        if result_k not in prune_set:
            partition_size += 1
            if partition_size == sys.argv[1]:
                partition_size = 0
                # prune
                sorted_views = sorted(result_dict.items(), key=lambda x: x[1][0], reverse=True)
                min_lower_bounds = []
                for view, bounds in sorted_views[:5]:
                    min_lower_bounds.append(bounds[1])

                top_5_lower_bound = min(min_lower_bounds)

                for view, bounds in sorted_views[5:]:
                    if bounds[0] < top_5_lower_bound:
                        prune_set.add(view)


            # outputs the key array married and unmarried.
            k_arr = list(k)
            k_arr[3] = 'married'
            k_1 = tuple(k_arr)
            k_arr[3] = 'unmarried'
            k_2 = tuple(k_arr)

            arr1, arr2 = get_normalized_list(query_obj[k_1], query_obj[k_2])
            result_dict[result_k] = [arr1 + arr2]
            n = len(result_dict[result_k][0])
            d = 0.05
            epislon = calc_running_confidence_interval(n//2, n, d)
            mean = np.mean(result_dict[result_k][0])
            result_dict[result_k]= [mean + epislon, mean - epislon]

    actual_res_dict = {}
    for k, v in result_dict.items():
        if k not in prune_set:
            actual_res_dict[k] = v

    return_dict = {}
    for amf in actual_res_dict.keys():

        amf_arr = list(amf)
        amf_arr.append('married')
        k_1 = tuple(amf_arr)
        amf_arr[3] = 'unmarried'
        k_2 = tuple(amf_arr)

        arr1, arr2 = get_normalized_list(query_obj[k_1], query_obj[k_2])
        return_dict[amf] = scipy.stats.entropy(arr1, arr2)

    return_dict = dict(sorted(return_dict.items(), key=lambda item: item[1], reverse=True))


    top_10 = dict(list(return_dict.items())[:5])

    print("Top 5 dictionary items with highest distance:")
    for key, value in top_10.items():
        print(key, "=", value)

    return return_dict


bruh = generate_queries(A,M,F,D)
get_res(bruh)

end_time = time.time()
print("running time with pruning: " + str(end_time - start_time))