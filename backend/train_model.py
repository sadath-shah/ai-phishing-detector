import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

df = pd.read_csv("../data/CEAS_08.csv")

df["subject"] = df["subject"].fillna("")

df["text"] = df["subject"] + " " + df["body"]

df = df[["text", "label"]]

df = df[df["text"].str.strip() != ""]

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Total emails:", len(df))
print("Training emails:", len(X_train))
print("Testing emails:", len(X_test))

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=50000
)

X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)

print("\n========== TF-IDF ==========")
print("Training shape:", X_train_tfidf.shape)
print("Testing shape:", X_test_tfidf.shape)

print("\n========== TRAINING MODEL ==========")

model = LogisticRegression(
    max_iter=1000,
    solver="liblinear",
    C=1.0
)

model.fit(X_train_tfidf, y_train)

print("Model training complete!")

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

print("\n========== MODEL PERFORMANCE ==========")

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")

print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Legitimate", "Phishing"]
    )
)

joblib.dump(
    model,
    "../models/phishing_model.pkl"
)

joblib.dump(
    vectorizer,
    "../models/tfidf_vectorizer.pkl"
)

print("\n========== SAVING MODEL ==========")

print("ML model saved to:")
print("../models/phishing_model.pkl")

print("TF-IDF vectorizer saved to:")
print("../models/tfidf_vectorizer.pkl")