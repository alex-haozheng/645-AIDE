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
def generate_queries(A, M, F):
    query_obj = {}
    for a in A:
        for m in M:
            for f in F:
                query = f"SELECT {a}, {f}({m}) FROM {d} GROUP BY {a}"
                query_obj[(a, f, m, d)] = [query]
    return query_obj

def normalization(arr1, arr2):
    sum1 = sum(arr1)
    sum2 = sum(arr2)
    norm_1 = [elem / sum1 for elem in arr1]
    norm_2 = [elem / sum2 for elem in arr2]
    return norm_1, norm_2

# Unoptimized part 2 exhaustive search
def problem_statement():
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



