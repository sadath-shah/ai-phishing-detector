import pandas as pd

df = pd.read_csv("../data/CEAS_08.csv")

print("Original dataset:")
print(df.shape)

df["subject"] = df["subject"].fillna("")

df["text"] = df["subject"] + " " + df["body"]

df = df[["text", "label"]]

df = df[df["text"].str.strip() != ""]

print("\nCleaned dataset:")
print(df.shape)

print("\nLabel distribution:")
print(df["label"].value_counts())

print("\nExample email:")
print(df.iloc[0]["text"][:500])

print("\nExample label:")
print(df.iloc[0]["label"])