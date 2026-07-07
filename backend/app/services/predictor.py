import numpy as np

from app.services.model_loader import model
from app.utils.knowledge_base import (
    ERROR_SOLUTIONS,
    DEFAULT_RESOLUTION
)
from app.config import (
    UNKNOWN_THRESHOLD,
    TOP_K
)
from app.api.schemas import (
    AlternativePrediction,
    PredictionResponse,
    ErrorResponse
)


def predict_error(request: str, response: str):

    combined_text = (
        f"REQUEST:\n{request}\n\nRESPONSE:\n{response}"
    ).strip()

    if not combined_text.replace(
        "REQUEST:\n", ""
    ).replace(
        "RESPONSE:\n", ""
    ).strip():

        return ErrorResponse(
            error="Please provide a request or response."
        )

    probabilities = model.predict_proba(
        [combined_text]
    )[0]

    top_indices = np.argsort(
        probabilities
    )[::-1]

    best_index = top_indices[0]

    category = model.classes_[best_index]

    confidence = float(
        probabilities[best_index]
    )

    alternatives = []

    for idx in top_indices[1:TOP_K]:

        alternatives.append(
            {
                "category": model.classes_[idx],
                "confidence": round(
                    float(probabilities[idx]) * 100,
                    2
                )
            }
        )

    if confidence < UNKNOWN_THRESHOLD:

        return PredictionResponse(
            category="Unknown Error",
            confidence=round(confidence * 100, 2),
            resolution="No matching category found.",
            alternatives=[
                AlternativePrediction(**alt)
                for alt in alternatives
            ]
        )

    resolution = ERROR_SOLUTIONS.get(
        category,
        DEFAULT_RESOLUTION
    )

    return PredictionResponse(
        category=category,
        confidence=round(confidence * 100, 2),
        resolution=resolution,
        alternatives=[
            AlternativePrediction(**alt)
            for alt in alternatives
        ]
    )


def debug_predictions(request: str, response: str):

    combined_text = (
        f"REQUEST:\n{request}\n\nRESPONSE:\n{response}"
    )

    probabilities = model.predict_proba(
        [combined_text]
    )[0]

    indices = probabilities.argsort()[-5:][::-1]

    results = []

    for idx in indices:

        results.append(
            {
                "category": model.classes_[idx],
                "confidence": round(
                    float(probabilities[idx]) * 100,
                    2
                )
            }
        )

    return results