import pandas as pd

df = pd.read_csv("data/candidates.csv")

print(df)

print("\nRows and Columns")
print(df.shape)

print("\nColumn Names")
print(df.columns)

print("\nFirst 5 Rows")
print(df.head())

print("\nInformation")
print(df.info())