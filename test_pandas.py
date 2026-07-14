import pandas as pd

df = pd.read_csv("data/candidates.csv")

print(df)

print("\nRows and Columns")
print(df.shape)

print("\nColumn Names")
print(df.columns)

print("\nTotal Candidates")
print(len(df))

print("\nAverage Age")
print(df["Age"].mean())

print("\nOldest Candidate Age")
print(df["Age"].max())

print("\nYoungest Candidate Age")
print(df["Age"].min())

print("\nCandidates Age > 20")
print(df[df["Age"] > 20])

print("\nCandidates Age == 21")
print(df[df["Age"] == 21])

print("\nCandidate Names")
print(df["Name"])

print("\nCandidate Ages")
print(df["Age"])