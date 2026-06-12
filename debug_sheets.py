import pandas as pd


#this file is just for testing the content of the excel file, I just wanted to test if the column names are on the first row.
file_name = 'Andromeda_Data.xlsx'
df = pd.read_excel(file_name, sheet_name='Laboratory')
print("Preview of the first 5 rows:")
print(df.head(5))