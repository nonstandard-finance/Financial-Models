import os
import pickle
import numpy as np
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/cashflow",
    tags=["Cash Flow"],
)

# Define the paths where your trained model and scalers were saved.
# (Make sure these files exist; see the "Saving additional objects" section below.)
MODEL_DIR = "Cash_Flow_Prediction_Model"
MODEL_PATH = os.path.join(MODEL_DIR, "cash_flow_model.pkl")
SCALER_X_PATH = os.path.join(MODEL_DIR, "scaler_x.pkl")
SCALER_Y_PATH = os.path.join(MODEL_DIR, "scaler_y.pkl")

# Load the trained model and preprocessing scalers on startup
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

try:
    with open(SCALER_Y_PATH, "rb") as f:
        scaler_y = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load target scaler from {SCALER_Y_PATH}: {e}")


# Define the expected input payload using Pydantic
class FinancialInput(BaseModel):
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
    return {"message": "Welcome to the Cash Flow Prediction API. Use the /predict endpoint."}


@router.post("/predict")
def predict_cash_flow(data: FinancialInput):
    try:
        # Compute the interaction features (the order here must match what was used in training)
        interaction_current_quick = data.current_ratio * data.quick_ratio
        interaction_return_debt = data.return_on_assets * data.debt_to_equity

        # Assemble the feature vector in the same order as during training:
        # [Current_Ratio, Quick_Ratio, Debt_to_Equity, Return_on_Assets,
        #  Operating_Margin, Lagged_Revenue, Lagged_Net_Income, Lagged_Operating_Cash_Flow,
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

        # Predict the (normalized) target value using the loaded model
        prediction_norm = model.predict(features_scaled)

        # Invert the target scaling (using StandardScaler) to get the prediction in original scale.
        # Note: we reshape the prediction to 2D since the scaler expects a 2D array.
        prediction = scaler_y.inverse_transform(prediction_norm.reshape(-1, 1))

        # Return the prediction as a JSON response
        return {"predicted_cash_flow": prediction[0, 0]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
