import numpy as np
import pandas as pd
import psycopg2


# TODO change variable to connect to presgresdb
DB_NAME = "census"
DB_HOST = "localhost"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME,host=DB_HOST,port=DB_PORT)

# example code for query
cur = conn.cursor()
cur.execute("select * from adults")
temp = cur.fetchall()
conn.commit()
# conn.close()

# includes married people
D_Q = "married"

# includes unmarried people
D_R = "unmarried"

d = 'adults'

# dimension attribute (for group by)
A = ['workclass','education','occupation','relationship','race','sex','native_country','income']
# Measure attribute (for aggregate)
M = ['age','fnlwgt', 'education_num','capital_gain','capital_loss','hours_per_week']
# aggregate function 
F = ['MIN', 'MAX', 'COUNT', 'SUM', 'AVG']

# iterate a, m, f into this query
# SELECT a, f(m), FROM D group by a

def get_aggregate():
	res = ''
	for f in F:
		for m in M:
				res += f'{f}({m}) as {f}_{m} ,'
	return res[:-1]

# print(get_aggregate())

# [a1, f1m1, f2m1, f3m1]
# [a2, f1m1, f2m1, f3m1]

# select workclass, max(age), case when marital_status = 'Married' then 0 else 1 end as g1, 1 as g2 from adults where workclass is not null group by workclass, g1, g2

def generate_queries(A, D):
	ret = {}
	for a in A:
		# 0 is married ; 1 is unmarried
		q = f"select {a}, {get_aggregate()}, case when marital_status = 'Married' then 0 else 1 end as married from {D} where {a} is not null group by {a}, married"
		cur.execute(q)
		# ret[a] = cur.fetchall()
		ret[a] = [cur.fetchmany(5),[desc[0] for desc in cur.description]]
		conn.commit()
		break
	return ret
	
d = generate_queries(A, d)

#{a: (m, aggregation... , label)}
def normalize(q):
	for k, v in q.items():
		x = np.array(list(v))
		print(x[:,0])
		print(x[:,-1])
		# for i in range(1, x.shape[1]-1):
		# 	col = x[:, i]
		# 	print(col)
	  
def reformat(q):
	ret = {}
	for a, v in q.items():
		# get the df with columns labeled
		df = pd.DataFrame(v[0], columns=v[1])
		print(df)
	return 

reformat(d)