import psycopg2 as psy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''this file contains the visualization 
how to transition from query data to plotting

NOTE: uses seaborn for better visualization
will need to generalize a function in the end with input of query (a, m, f)'''

# connect to db
con = psy.connect(database='census', host='localhost')

with con.cursor() as cur:
	cur.execute('select sex, avg(capital_gain) from married group by sex;')
	tgt = cur.fetchall()

	cur.execute('select sex, avg(capital_gain) from unmarried group by sex;')
	ref = cur.fetchall()

	# plot the graph using the list
	n = max(len(tgt), len(ref))
	# avg_tgt = tgt.values()
	# avg_ref = ref.values()
	tgt_df = pd.DataFrame(tgt, columns=['category', 'value'])
	ref_df = pd.DataFrame(ref, columns=['category', 'value'])
	merged_df = pd.merge(tgt_df, ref_df, how='outer', on='category')
	merged_df.columns = ['category', 'married', 'unmarried']
	# fill in blanks
	merged_df.fillna("0", inplace=True)
	print(merged_df)
	melted_df = pd.melt(merged_df, id_vars=['category'], value_vars=['married', 'unmarried'], var_name='marital_status', value_name='value')
	print(melted_df)
	sns.catplot(x='category', y='value', hue='marital_status', data=melted_df, kind='bar')
	plt.show()
	# x = np.arange(n)
	# plt.bar(x-0.05, avg_ref, 0.1, color='green')
	# plt.bar(x+0.05, avg_tft, 0.1, color='cyan')
	# plt.xticks(x, list(tgt.keys()))
	# plt.legend()
	# plt.show()

