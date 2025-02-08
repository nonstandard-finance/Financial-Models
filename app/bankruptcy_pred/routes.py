import os
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/bankruptcy",
    tags=["Bankruptcy"],
)

# Define the paths where the trained model and scaler were saved.
# (Be sure to update your training code to save the scaler used for features, e.g., scaler_X)
MODEL_DIR = "Bankruptcy_Prediction_Model"
MODEL_PATH = os.path.join(MODEL_DIR, "bankruptcy_model.pkl")
SCALER_X_PATH = os.path.join(MODEL_DIR, "scaler_x.pkl")

# Load the trained classifier and feature scaler at startup
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {e}")

try:
    with open(SCALER_X_PATH, "rb") as f:
        scaler_x = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load feature scaler from {SCALER_X_PATH}: {e}")


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
        # Interaction_Current_Quick = current_ratio * quick_ratio
        # Interaction_Return_Debt = return_on_assets * debt_to_equity
        interaction_current_quick = data.current_ratio * data.quick_ratio
        interaction_return_debt = data.return_on_assets * data.debt_to_equity

        # Assemble the feature vector in the same order as used during training:
        # [Current_Ratio, Quick_Ratio, Debt_to_Equity, Return_on_Assets, Operating_Margin,
        #  Lagged_Revenue, Lagged_Net_Income, Lagged_Operating_Cash_Flow,
        #  Interaction_Current_Quick, Interaction_Return_Debt]
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

        # If your classifier supports probability estimates, you can also compute them.
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
