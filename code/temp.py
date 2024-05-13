import numpy as np
import psycopg2
import scipy

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
                    query_obj[(a, f, m, d)] = cur.fetchall()
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


def get_res(query_obj):
    # result_dict[(a,m,f)] = distance
    result_dict = {}
    # k = (a,m,f,d) v = [query, queryres]
    for k, v in query_obj.items():
        result_k = k[:-1]
        if result_k in result_dict:
            continue

        # outputs the key array married and unmarried.
        k_arr = list(k)
        k_arr[3] = 'married'
        k_1 = tuple(k_arr)
        k_arr[3] = 'unmarried'
        k_2 = tuple(k_arr)

        arr1, arr2 = get_normalized_list(query_obj[k_1], query_obj[k_2])

        # KL divergence
        distance = scipy.stats.entropy(arr1, arr2)
        result_dict[result_k] = distance

    sorted_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))

    # Get the top 10 items from the sorted dictionary
    top_10 = dict(list(sorted_dict.items())[:10])

    print("Top 10 dictionary items with highest distance:")
    for key, value in top_10.items():
        print(key, "=", value)

    return result_dict


get_res(generate_queries(A, M, F, D))
