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
con = psy.connect(database='yiding', host='localhost')

with con.cursor() as cur:
	cur.execute('select native_country, max(capital_gain) from married group by native_country')
	tgt = cur.fetchall()

	cur.execute('select native_country, max(capital_gain) from unmarried group by native_country')
	ref = cur.fetchall()

	# plot the graph using the list

	# this finds the max length of the queries or max categories
	n = max(len(tgt), len(ref))

	# avg_tgt = tgt.values()
	# avg_ref = ref.values()

	# convert to dataframse labeled with category, value (projection of a query with group, aggregate value)
	tgt_df = pd.DataFrame(tgt, columns=['category', 'value'])
	ref_df = pd.DataFrame(ref, columns=['category', 'value'])
	# merge for plotting ("outer" join on "category")
	merged_df = pd.merge(tgt_df, ref_df, how='outer', on='category')
	merged_df.columns = ['category', 'married', 'unmarried']
	# fill in blanks if one of the dataframes missing a category
	merged_df.fillna(0, inplace=True)
	print(merged_df)
	# this is to convert it into rows for plotting in catplot (w/ help from chatgpt)
	melted_df = pd.melt(merged_df, id_vars=['category'], value_vars=['married', 'unmarried'], var_name='marital_status', value_name='value')
	print(melted_df)
	graph = sns.catplot(x='category', y='value', hue='marital_status', data=melted_df, kind='bar')
	graph.set_xticklabels(rotation=45)
	plt.show()
	# x = np.arange(n)
	# plt.bar(x-0.05, avg_ref, 0.1, color='green')
	# plt.bar(x+0.05, avg_tft, 0.1, color='cyan')
	# plt.xticks(x, list(tgt.keys()))
	# plt.legend()
	# plt.show()

