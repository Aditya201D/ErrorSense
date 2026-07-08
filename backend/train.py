import pandas as pd
import joblib
import json
import re
from datetime import datetime
import xml.etree.ElementTree as ET

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report
)
from sklearn.pipeline import Pipeline

# We will remove the random and useless fields from the request strings.
FIELDS_TO_REMOVE = [
    "uid",
    "otp",
    "codeHash",
    "loginToken",
    "otpTxnId",
    "rid",
    "mac",
    "certificate",
    "signature",
    "transactionId",
    "aadharUserId"
]


# We will extract the important defining (which help in classifying) features of requests
IMPORTANT_REQUEST_FIELDS = [
    "entity",
    "interfaceType",
    "version",
    "stateShortName",
    "saleTypeId"
]

# A map to make parsing easier for TF-IDF.
FIELD_NAMES = {
    "entity": "ENTITY",
    "interfaceType": "INTERFACE",
    "version": "VERSION",
    "stateShortName": "STATE",
    "saleTypeId": "SALE_TYPE",
}

# We will use presence flags to just indicate the presence of a field in a request, no need to remember its value
PRESENCE_FIELDS = [
    "pin",
    "uid",
    "otp",
    "certificate",
    "PidData"
]

# ========== REQUEST PARSER ==============

def extract_request_features(text: str) -> str:
    if not text.strip():
        return ""
    features = []
    
    # If request is JSON
    if text.strip().startswith("{"):
        try:
            data = json.loads(text)
            features.append("REQUEST_TYPE=JSON")
            for field in IMPORTANT_REQUEST_FIELDS:
                value = data.get(field)
                if value not in [None, ""]:
                    features.append(
                        f"{FIELD_NAMES[field]}={value}"
                    )

            for field in PRESENCE_FIELDS:
                if field in data:
                    features.append(
                        f"HAS={field.upper()}"
                    )

            return " ".join(features)

        except Exception:
            return ""

    # If request is XML
    if text.strip().startswith("<"):
        try:
            root = ET.fromstring(text)
            features.append("REQUEST_TYPE=XML")
            for field in IMPORTANT_REQUEST_FIELDS:
                element = root.find(field)
                if (
                    element is not None
                    and element.text
                ):
                    features.append(
                        f"{FIELD_NAMES[field]}={element.text}"
                    )

            for field in PRESENCE_FIELDS:
                if root.find(field) is not None:
                    features.append(
                        f"HAS={field.upper()}"
                    )

            return " ".join(features)
        
        except Exception:
            return ""
    return ""

# ============= RESPONSE PARSER ===================

def extract_response_features(text: str) -> str:
    if not text.strip():
        return ""

    features = []
    cleaned_text = text.strip()

    # Some rows contain multiple JSON objects. We'll parse only the first one.
    decoder = json.JSONDecoder()
    try:
        response, _ = decoder.raw_decode(cleaned_text)
        features.append("RESPONSE_TYPE=JSON")
        status = response.get("statusCode")
        if status:
            features.append(
                f"STATUS={status}"
            )

        description = response.get("description")
        if description:
            features.append(
                f"DESCRIPTION={description}"
            )

        field_errors = response.get("fieldErrors")
        if isinstance(field_errors, dict):
            for values in field_errors.values():
                if isinstance(values, list):
                    for error in values:
                        features.append(
                            f"FIELD_ERROR={error}"
                        )

        return (
            " ".join(features) + "\n" + cleaned_text
        )

    except Exception:
        # Not valid JSON.
        # Still keep the response text.
        return cleaned_text
    
# ============= NORMALIZING DESCRIPTION FEATURE ================

def normalize_description(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    
    # OTP Cooldown type
    text = re.sub(
        r"Try after\s+\d+\s+Mins?",
        "Try after N Mins",
        text,
        flags=re.IGNORECASE
    )

    # Aadhar type
    text = re.sub(
        r"XXXXXXXX\d{4}",
        "XXXXXXXX",
        text
    )

    # Plant/Product type
    text = re.sub(
        r"\(Plant:.*",
        "",
        text
    )
    
    # Input string values
    text = re.sub(
        r'For input string:\s*".*?"',
        "For input string",
        text
    )

    # Multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )
    return text.strip()



df = pd.read_excel(
    "data/Request and Response of failures.xlsx"
)

print(df.columns)

df = df[
    [
        "request_string",
        "response_string",
        "description"
    ]
]

df["request_string"] = (
    df["request_string"]
    .fillna("")
    .astype(str)
    .apply(extract_request_features)
)

df["response_string"] = (
    df["response_string"]
    .fillna("")
    .astype(str)
    .apply(extract_response_features)
)

df["description"] = (
    df["description"]
    .fillna("")
    .astype(str)
    .apply(normalize_description)
)

# Combining the request and response columns
df["combined_text"] = (
    "REQUEST\n"
    + df["request_string"]
    + "\n\n"
    + "RESPONSE\n"
    + df["response_string"]
)

# Removing description categories with less than 2 samples
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

print("\nTop 20 categories:\n")
print(
    df["description"]
    .value_counts()
    .head(20)
)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    df["combined_text"],
    df["description"],
    test_size=0.2,
    random_state=42,
    stratify=df["description"]
)

# MODEL PIPELINE
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

print("\nTraining model...")

pipeline.fit(
    X_train,
    y_train
)

predictions = pipeline.predict(
    X_test
)


# SAVING A REPORT
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

# SAVE MODEL
joblib.dump(
    pipeline,
    "model/error_classifier.pkl"
)

print(
    "\nModel saved successfully."
)