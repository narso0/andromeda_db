import pandas as pd

file_name = 'Andromeda_Data.xlsx'
# header=None tells Pandas: "Don't look for headers, just show me the raw data"
df = pd.read_excel(file_name, sheet_name='Laboratory', header=None)
print("--- Raw preview of the first 5 rows ---")
print(df.head(5))