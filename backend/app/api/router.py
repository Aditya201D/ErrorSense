from fastapi import APIRouter

from app.api.schemas import (
    UserInput,
    PredictionResponse,
    ErrorResponse,
    StatusResponse,
)

from app.services.predictor import (
    predict_error,
    debug_predictions
)

router = APIRouter()


@router.get(
    "/",
    response_model=StatusResponse
)
def home():

    return {
        "status": "running"
    }


@router.post(
    "/predict",
    response_model=PredictionResponse | ErrorResponse
)
def predict(data: UserInput):

    return predict_error(
        data.request,
        data.response
    )


@router.post(
    "/debug"
)
def debug(data: UserInput):

    return debug_predictions(
        data.request,
        data.response
    )