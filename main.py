import pandas as pd # type: ignore

cols = ["colc", "ra", "field", "fieldid", "dec"]
data = pd.read_csv('sdss_100k.csv.gz', compression='gzip')[cols]

print(len(data.index))