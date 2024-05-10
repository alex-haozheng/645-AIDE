import numpy as np
import psycopg2
import scipy


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
A = ['workclass','education','occupation','relationship','race','sex','native_country','salary_range']
# Measure attribute (for aggregate)
M = ['age','fnlwgt', 'education_num','capital_gain','capital_loss','hours_per_week']
# aggregate function 
F = ['MIN', 'MAX', 'COUNT', 'SUM', 'AVG']

# iterate a, m, f into this query
# SELECT a, f(m), FROM D group by a

def generate_queries(A, M, F, D_Q, D_R):
    queries = []
    for a in A:
        for m in M:
            for f in F:
                query1 = f"SELECT {a}, {f}({m}), FROM {D_Q} GROUP BY {a}"
                query2 = f"SELECT {a}, {f}{m}), FROM {D_R} GROUP BY {a}"
                queries.append((query1, query2))
    return queries

queries = generate_queries(A, M, F, D_Q, D_R)

for query in queries:
    print(query)
# Unoptimized part 2 exhaustive search
def problem_statement():
    # iterate through all possible a and m
    
    queries = generate_queries(A, M, F, D_Q, D_R)
    for query in queries:
        try:
            cur = conn.cursor()
            cur.execute(query[0])
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
        return

def normalization(a, b):

