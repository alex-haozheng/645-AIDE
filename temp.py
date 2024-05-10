import numpy as np
import psycopg2


# TODO connect it to your local postgresdb
DB_NAME = "tkgafrwp"
DB_USER = "tkgafrwp"
DB_PASS = "iYYtLAXVbid-i6MV3NO1EnU-_9SW2uEi"
DB_HOST = "tyke.db.elephantsql.com"
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
'''
cur = conn.cursor()
cur.execute("""
    INSERT INTO Employee (ID,NAME,EMAIL) VALUES
    (1,'Alan Walker','awalker@gmail.com'), 
    (2,'Steve Jobs','sjobs@gmail.com')
  """)
conn.commit()
conn.close()
'''

# includes married people
D_Q = None

# includes unmarried people
D_R = None

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

def problem_statement():
    
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Employee (ID,NAME,EMAIL) VALUES
        (1,'Alan Walker','awalker@gmail.com'), 
        (2,'Steve Jobs','sjobs@gmail.com')
    """)
    conn.commit()
    conn.close()
    return


# for calculating the deviation (distnace) using K-L divergence
def KL(a, b):
    a = np.asarray(a, dtype=np.float)
    b = np.asarray(b, dtype=np.float)

    return np.sum(np.where(a != 0, a * np.log(a / b), 0))
