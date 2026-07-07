from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import joblib
import numpy as np

from knowledge_base import (
    ERROR_SOLUTIONS,
    DEFAULT_RESOLUTION
)

app = FastAPI(
    title="Request Response Categoriser API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load(
    "model/error_classifier.pkl"
)


class UserInput(BaseModel):
    request: str = ""
    response: str = ""


@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.post("/predict")
def predict(data: UserInput):

    combined_text = (
        f"{data.request} {data.response}"
    ).strip()

    if not combined_text:

        return {
            "error":
            "Please provide a request or response."
        }

    probabilities = model.predict_proba(
        [combined_text]
    )[0]

    # Get indices sorted by confidence (highest first)
    top_indices = np.argsort(
        probabilities
    )[::-1]

    best_index = top_indices[0]

    category = model.classes_[
        best_index
    ]

    confidence = float(
        probabilities[best_index]
    )

    # Build alternative predictions
    alternatives = []

    for idx in top_indices[1:3]:

        alternatives.append(
            {
                "category": model.classes_[idx],
                "confidence": round(
                    float(probabilities[idx]) * 100,
                    2
                )
            }
        )

    # Unknown error detection
    if confidence < 0.15:

        return {
            "category": "Unknown Error",
            "confidence": round(
                confidence * 100,
                2
            ),
            "resolution":
                "No matching category found.",
            "alternatives": alternatives
        }

    resolution = ERROR_SOLUTIONS.get(
        category,
        DEFAULT_RESOLUTION
    )

    return {
        "category": category,
        "confidence": round(
            confidence * 100,
            2
        ),
        "resolution": resolution,
        "alternatives": alternatives
    }

@app.post("/debug")
def debug(data: UserInput):

    combined_text = (
        f"{data.request} {data.response}"
    ).strip()

    probabilities = model.predict_proba(
        [combined_text]
    )[0]

    indices = probabilities.argsort()[-5:][::-1]

    results = []

    for idx in indices:

        results.append({
            "category": model.classes_[idx],
            "confidence": round(
                float(probabilities[idx]) * 100,
                2
            )
        })

    return results