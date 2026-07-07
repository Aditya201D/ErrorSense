import pandas as pd
import joblib
import json
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report
)
from sklearn.pipeline import Pipeline

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_excel(
    "data/Request and Response of failures.xlsx"
)

# Keep required columns
df = df[
    [
        "request_string",
        "response_string",
        "description"
    ]
]

# Fill missing values
df["request_string"] = (
    df["request_string"]
    .fillna("")
    .astype(str)
)

df["response_string"] = (
    df["response_string"]
    .fillna("")
    .astype(str)
)

df["description"] = (
    df["description"]
    .fillna("")
    .astype(str)
)

# =====================================
# COMBINE REQUEST + RESPONSE
# =====================================

df["combined_text"] = (
    "REQUEST:\n"
    + df["request_string"]
    + "\n\nRESPONSE:\n"
    + df["response_string"]
)

# =====================================
# REMOVE RARE CATEGORIES
# =====================================

category_counts = (
    df["description"]
    .value_counts()
)

valid_categories = (
    category_counts[
        category_counts >= 2
    ].index
)

df = df[
    df["description"]
    .isin(valid_categories)
]

print(
    f"Dataset size after cleaning: {len(df)}"
)

print(
    f"Unique categories: {df['description'].nunique()}"
)

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    df["combined_text"],
    df["description"],
    test_size=0.2,
    random_state=42,
    stratify=df["description"]
)

# =====================================
# MODEL PIPELINE
# =====================================

pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=15000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=3000,
            random_state=42
        )
    )
])

# =====================================
# TRAIN
# =====================================

print("\nTraining model...")

pipeline.fit(
    X_train,
    y_train
)

# =====================================
# EVALUATION
# =====================================

predictions = pipeline.predict(
    X_test
)

report = classification_report(
    y_test,
    predictions,
    output_dict=False,
    zero_division=0
)

assert isinstance(report, str)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Accuracy: {accuracy:.4f}"
)

with open(
    "reports/classification_report.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print(
    "Classification report saved."
)

metadata = {
    "model": "Logistic Regression",
    "vectorizer": "TF-IDF",
    "accuracy": round(accuracy, 4),
    "dataset_size": len(df),
    "categories": df["description"].nunique(),
    "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open(
    "reports/model_metadata.json",
    "w"
) as f:
    json.dump(
        metadata,
        f,
        indent=4
    )

print(
    "Model metadata saved."
)

# =====================================
# SAVE MODEL
# =====================================

joblib.dump(
    pipeline,
    "model/error_classifier.pkl"
)

print(
    "\nModel saved successfully."
)