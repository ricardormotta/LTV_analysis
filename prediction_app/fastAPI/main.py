import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from ..features_utils import ProductEnum, ChannelEnum, AgeEnum, OperatingSystemEnum, NumericalFeatures, BooleanFeatures
from ..start_kedro_session import get_kedro_catalog
from ..predict_utils import predict_from_survival_model

# Get the kedro catalog 
catalog = get_kedro_catalog()
classifier = catalog.load("trained_classifier_pipeline")
survival_model = catalog.load("survival_model")
survival_threshold = catalog.load("params:survival_threshold")
cat_features = catalog.load("params:cat_cols")
app = FastAPI()


# Define the request body schema using Pydantic BaseModel
class InputData(BaseModel):
    days_to_churn: int
    product_x: int
    product_y: int
    numerical_features: NumericalFeatures
    product: ProductEnum
    channel: ChannelEnum
    age_bucket: AgeEnum
    operating_system: OperatingSystemEnum
    is_xs: bool


# Define a POST endpoint to make predictions
@app.post("/predict")
def predict(data: InputData):
    # Make prediction using the loaded model
    data = pd.DataFrame.from_dict(json.loads(data.json()), orient="index").T
    proba = classifier.predict_proba(data)[0,1]
    prediction = classifier.predict(data)
    days_to_churn = predict_from_survival_model(data, survival_model, cat_features, survival_threshold)
    return {"prediction": prediction, "predicted_days_to_churn": days_to_churn}
