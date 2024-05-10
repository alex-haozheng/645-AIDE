import pandas as pd

input_file = '../rawdata/adult.data'
output_file = '../data/fullset.csv'

# read the csv
df = pd.read_csv(input_file, header=None)

# replace all ? as None in the db
df.replace(' ?', None, inplace=True)

# Write the modified DataFrame to a new CSV file
df.to_csv(output_file, index=False, header=False)

married_attr = [' Widowed', ' Separated', ' Married-civ-spouse', ' Married-spouse-absent', ' Married-AF-spouse', ' Never-married']
unmarried_attr = [' Divorced',' Never-married']

marital_status = df.iloc[:, 5]
for m in married_attr:
	marital_status[marital_status == m] = 'Married'
for u in married_attr:
	marital_status[marital_status == u] = 'Unmarried'

df.head()
df.to_csv('../data/processed.csv', index=False, header=False)