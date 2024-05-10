import pandas as pd

input_file = '../rawdata/adult.data'
output_file = '../data/processed.csv'

headers = ["age", "workclass", "fnlwgt", "education", "education_num", "marital_status",
           "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", 
           "hours_per_week", "native_country", "salary"]

# read the csv
df = pd.read_csv(input_file, header=0, names = headers, delimiter=', ')

# replace all ? as None in the db
df.replace('?', None, inplace=True)

married_attr = ['Widowed', 'Separated', 'Married-civ-spouse', 'Married-spouse-absent', 'Married-AF-spouse', 'Never-married']
unmarried_attr = ['Divorced','Never-married']

for m in married_attr:
	df['marital_status'] = df['marital_status'].replace(m, 'Married')
for u in married_attr:
	df['marital_status'] = df['marital_status'].replace(u, 'Unmarried')
df.to_csv('../data/processed.csv', index=False, header=False)