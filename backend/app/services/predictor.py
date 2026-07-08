import numpy as np

from app.services.model_loader import model

from app.utils.knowledge_base import (
    ERROR_KB,
    DEFAULT_RECORD
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
            AlternativePrediction(
                category=model.classes_[idx],
                confidence=round(
                    float(probabilities[idx]) * 100,
                    2
                )
            )
        )

    record = ERROR_KB.get(
        category,
        DEFAULT_RECORD
    )

    if confidence < UNKNOWN_THRESHOLD:

        return PredictionResponse(

            category="Unknown Error",

            confidence=round(
                confidence * 100,
                2
            ),

            severity="Unknown",

            module="Unknown",

            resolution=DEFAULT_RECORD[
                "resolution"
            ],

            next_step=DEFAULT_RECORD[
                "next_step"
            ],

            documentation=DEFAULT_RECORD[
                "documentation"
            ],

            alternatives=alternatives
        )

    return PredictionResponse(

        category=category,

        confidence=round(
            confidence * 100,
            2
        ),

        severity=record["severity"],

        module=record["module"],

        resolution=record["resolution"],

        next_step=record["next_step"],

        documentation=record["documentation"],

        alternatives=alternatives
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

        category = model.classes_[idx]

        record = ERROR_KB.get(
            category,
            DEFAULT_RECORD
        )

        results.append(
            {
                "category": category,
                "confidence": round(
                    float(probabilities[idx]) * 100,
                    2
                ),
                "severity": record["severity"],
                "module": record["module"]
            }
        )

    return results