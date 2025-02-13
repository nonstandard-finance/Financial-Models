import os
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

from sklearn.preprocessing import PowerTransformer

router = APIRouter(
    prefix="/bankruptcy",
    tags=["Bankruptcy"],
)

# Define the paths where the trained model and scaler were saved.
# (Be sure to update your training code to save the scaler used for features, e.g., scaler_X)
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "bankruptcy_model.pkl")


# Load the trained classifier and feature scaler at startup
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {e}")


# Define the expected input payload using Pydantic
class BankruptcyInput(BaseModel):
    current_ratio: float
    quick_ratio: float
    debt_to_equity: float
    return_on_assets: float
    operating_margin: float
    lagged_revenue: float
    lagged_net_income: float
    lagged_operating_cash_flow: float


@router.get("/")
def read_root():
    return {"message": "Welcome to the Bankruptcy Prediction API. Use the /predict endpoint."}


@router.post("/predict")
def predict_bankruptcy(data: BankruptcyInput):
    try:
        # Compute the interaction features:
        interaction_current_quick = data.current_ratio * data.quick_ratio
        interaction_return_debt = data.return_on_assets * data.debt_to_equity

        scaler_x = PowerTransformer()

        # Assemble the feature vector in the same order as used during training:

        features = np.array([[
            data.current_ratio,
            data.quick_ratio,
            data.debt_to_equity,
            data.return_on_assets,
            data.operating_margin,
            data.lagged_revenue,
            data.lagged_net_income,
            data.lagged_operating_cash_flow,
            interaction_current_quick,
            interaction_return_debt
        ]])

        # Apply the same feature preprocessing (PowerTransformer) used during training
        features_scaled = scaler_x.transform(features)

        # Predict the bankruptcy class using the loaded classifier
        prediction = model.predict(features_scaled)

        # Here we assume that the positive class (1) means bankruptcy.
        bankruptcy_probability = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(features_scaled)
            bankruptcy_probability = proba[0][1]  # probability for class 1

        return {
            "predicted_class": int(prediction[0]),
            "bankruptcy_probability": bankruptcy_probability
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
