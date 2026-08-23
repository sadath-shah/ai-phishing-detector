import pandas as pd


df = pd.read_csv("../data/CEAS_08.csv")


print("\n========== DATASET SHAPE ==========")
print(df.shape)


print("\n========== COLUMNS ==========")
print(df.columns.tolist())


print("\n========== FIRST 5 ROWS ==========")
print(df.head())


print("\n========== DATASET INFO ==========")
print(df.info())


print("\n========== LABEL DISTRIBUTION ==========")
print(df["label"].value_counts())


print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())