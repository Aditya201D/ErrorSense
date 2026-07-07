from fastapi import APIRouter

from app.api.schemas import UserInput
from app.services.predictor import (
    predict_error,
    debug_predictions
)

router = APIRouter()


@router.get("/")
def home():

    return {
        "status": "running"
    }


@router.post("/predict")
def predict(data: UserInput):

    return predict_error(
        data.request,
        data.response
    )


@router.post("/debug")
def debug(data: UserInput):

    return debug_predictions(
        data.request,
        data.response
    )