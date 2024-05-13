import numpy as np
import pandas as pd
import psycopg2
import scipy


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
		q = f"select {a}, {get_aggregate()}, case when marital_status = 'Married' then 1 else 0 end as married from {D} where {a} is not null group by {a}, married"
		cur.execute(q)
		# ret[a] = cur.fetchall()
		# ret[a] = [cur.fetchmany(5),[desc[0] for desc in cur.description]]
		ret[a] = [cur.fetchall(),[desc[0] for desc in cur.description]]
		conn.commit()
	return ret
	
d = generate_queries(A, d)

def normalization(arr1, arr2):
	sum1 = sum(arr1)
	sum2 = sum(arr2)
	norm_1 = [elem / sum1 for elem in arr1]
	norm_2 = [elem / sum2 for elem in arr2]

	return norm_1, norm_2
	  
def get_topK(q):
	ret = {}
	for a, v in q.items():
		# get the df with columns labeled
		df = pd.DataFrame(v[0], columns=v[1])
		# create separate dataframe for married and unmarried
		married_df = df[df['married'] == 1]
		unmarried_df = df[df['married'] == 0]

		#merge the two
		result_df = pd.merge(married_df, unmarried_df, on=a, suffixes=('_md', '_umd'), how='inner')
		# change to all non zero values 
		# df.replace(0, 1e-10, inplace=True)

		# .columns returns list of string columsn 
		for column in result_df.columns[1:31]:
			#break into strings
			c = column.split('_')
			f, m, _ = c[0], '_'.join(c[1:-1]), c[-1]
			# print(f, m, _)
			ta = result_df[f'{f}_{m}_md'].astype(float).tolist()
			tb = result_df[f'{f}_{m}_umd'].astype(float).tolist()
			for i,t in enumerate(ta):
				if int(t) == 0:
					ta[i] = 1e-10
			for i,t in enumerate(tb):
				if int(t) == 0:
					tb[i] = 1e-10
			n_mar, n_unm = normalization(ta, tb)
			distance = scipy.stats.entropy(n_mar, n_unm)
			ret[(a,m,f)] = distance
	sorted_dict = dict(sorted(ret.items(), key=lambda item: item[1], reverse=True))

	# Get the top 10 items from the sorted dictionary
	top_10 = dict(list(sorted_dict.items())[:10])

	print("Top 10 dictionary items with highest distance:")
	for key, value in top_10.items():
			print(key, "=", value)

	return ret



#[24(federal gov), 20(self emp), 25(state gov)] [8(fed), 17]

get_topK(d)