import numpy as np
import psycopg2
import scipy
import numpy as np

# TODO change variable to connect to presgresdb
DB_NAME = "census"
DB_USER = ""
DB_PASS = ""
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connected successfully")
except:
    print("Database not connected successfully")

# example code for query
#
# cur = conn.cursor()
# cur.execute("SELECT * FROM adults")
# temp = cur.fetchall()
# conn.commit()
# conn.close()

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

# dictionary to store the query result and A M F D of the

'''
obj query_obj = {a: element in A, m: element in M, f: element in F, d: database name, 
query: sql query, query_res: result list of tuples, distance: distance}
'''


# iterate a, m, f into this query
# SELECT a, f(m), FROM D group by a
def generate_queries(A, M, F, D):
    query_obj = {}
    for a in A:
        for m in M:
            for f in F:
                for d in D:
                    query = f"SELECT {a}, {f}({m}) FROM {d} GROUP BY {a}"
                    query_obj[(a, f, m, d)] = [query]
    return query_obj


def normalization(arr1, arr2):
    sum1 = sum(arr1)
    sum2 = sum(arr2)
    norm_1 = arr1
    norm_2 = arr2
    if sum1 != 0:
        norm_1 = [elem / sum1 for elem in arr1]
    if sum2 != 0:
        norm_2 = [elem / sum2 for elem in arr2]

    return norm_1, norm_2


# Unoptimized part 2 exhaustive search
def get_db_res():
    # iterate through all possible a and m
    query_obj = generate_queries(A, M, F, D)
    cur = conn.cursor()
    for k, v in query_obj.items():
        cur.execute(query_obj[k][0])
        query_res = cur.fetchall()
        conn.commit()
        query_obj[k].append(query_res)
    conn.close()

    return query_obj


def get_normalized_list(query_obj1: list[tuple], query_obj2: list[tuple]):
    arr1 = []
    arr2 = []

    query_tuple_list_1 = [elem for elem in query_obj1[1] if elem[0] is not None]
    query_tuple_list_1 = sorted(query_tuple_list_1, key=lambda x: x[0])

    query_tuple_list_2 = [elem for elem in query_obj2[1] if elem[0] is not None]
    query_tuple_list_2 = sorted(query_tuple_list_2, key=lambda x: x[0])

    min_iter = min(len(query_tuple_list_1), len(query_tuple_list_2))

    for i in range(min_iter):
        tuple1 = query_tuple_list_1[i]
        tuple2 = query_tuple_list_2[i]

        if tuple1[0] == tuple2[0]:
            if tuple1[0] != 0:
                arr1.append(float(tuple1[1]))
            else:
                arr1.append(float(1e-10))
            if tuple2[0] != 0:
                arr2.append(float(tuple2[1]))
            else:
                arr2.append(float(1e-10))

    arr1, arr2 = normalization(arr1, arr2)
    return arr1, arr2


def get_res(query_obj):
    result_dict = {}
    for k, v in query_obj.items():
        result_k = k[:-1]
        if result_k in result_dict:
            continue

        k_arr = list(k)
        k_arr[3] = 'married'
        k_1 = tuple(k_arr)
        k_arr[3] = 'unmarried'
        k_2 = tuple(k_arr)

        arr1, arr2 = get_normalized_list(query_obj[k_1], query_obj[k_2])

        distance = scipy.stats.entropy(arr1, arr2)
        result_dict[result_k] = distance

    sorted_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))

    # Get the top 10 items from the sorted dictionary
    top_10 = dict(list(sorted_dict.items())[:10])

    print("Top 10 dictionary items with highest distance:")
    for key, value in top_10.items():
        print(key, "=", value)

    return result_dict


get_res(get_db_res())
