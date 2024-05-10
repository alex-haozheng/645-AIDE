import numpy as np
import psycopg2


# TODO change variable to connect to presgresdb
DB_NAME = "census"
DB_HOST = "localhost"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME,host=DB_HOST,port=DB_PORT)

# example code for query
#
# cur = conn.cursor()
# cur.execute("SELECT * FROM adults")
# temp = cur.fetchall()
# conn.commit()
# conn.close()

# includes married people
D_Q = None

# includes unmarried people
D_R = None

D = [D_Q, D_R]

# dimension attribute (for group by)
A = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", 
     "race", "sex", "capital-gain", "captial-loss", "hours-per-week", "native-country"]
# Measure attribute (for aggregate)
M = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", 
     "race", "sex", "capital-gain", "captial-loss", "hours-per-week", "native-country"]
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


# for calculating the deviation (distnace) using K-L divergence
def KL(a, b):
    a = np.asarray(a, dtype=np.float)
    b = np.asarray(b, dtype=np.float)

    return np.sum(np.where(a != 0, a * np.log(a / b), 0))
