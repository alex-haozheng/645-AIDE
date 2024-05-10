import pandas as pd

input_file = 'rawdata/adult.data'
output_file = 'data/fullset.csv'

# read the csv
df = pd.read_csv(input_file, header=None)

# replace all ? as None in the db
df.replace('?', None, inplace=True)

# Write the modified DataFrame to a new CSV file
df.to_csv(output_file, index=False, header=False)