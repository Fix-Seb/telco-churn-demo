"""API for making churn predictions using a FastAPI server.

Add fastapi and uvicorn to your environment with:
    uv add fastapi uvicorn

To serve the API, run:
    uv run uvicorn api:app --reload
"""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field

from prediction import make_prediction


# Field names match those used in the model training
# Aliases are more user-friendly names for the API
class Customer(BaseModel):
    tenure: int
    MonthlyCharges: float = Field(alias="monthly")
    TechSupport_yes: int = Field(alias="techsupport")


app = FastAPI()


@app.post("/predict")
def predict(customer: Customer):
    """Make a churn prediction for a customer."""
    prediction = make_prediction(**customer.model_dump())
    return {"prediction": prediction}


@app.get("/schema")
def predict_schema():
    """Describe the expected fields for /predict."""
    return Customer.model_json_schema()


@app.get("/health")
def health(response: Response):
    """Report whether the API can make a prediction."""
    try:
        make_prediction(tenure=1, MonthlyCharges=1.0, TechSupport_yes=1)
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ok"}
    return {"status": "ok"}
