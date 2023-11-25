import os
import json
from fastapi import FastAPI
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pydantic import BaseModel
import pandas as pd
from .features_utils import ProductEnum, ChannelEnum, AgeEnum, OperatingSystemEnum, NumericalFeatures, BooleanFeatures

# Create a Kedro context
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kedro_project_name = "ltv-ml-project"
project_path = os.path.join(base_dir, kedro_project_name)
bootstrap_project(project_path)
session = KedroSession.create(
    package_name=kedro_project_name,
    project_path=project_path,
)

# Load the Kedro project context
context = session.load_context()
classifier = context.catalog.load("trained_classifier_pipeline")
survival_model = context.catalog.load("survival_model")
survival_threshold = context.catalog.load("params:survival_threshold")
train_cols_surv_model = survival_model.variance_matrix_.columns
cat_features = context.catalog.load("params:cat_cols")
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
    data_to_surv_model = pd.get_dummies(data, columns=cat_features)
    missing_cols = train_cols_surv_model[~train_cols_surv_model.isin(data_to_surv_model.columns)]
    for col in missing_cols:
        data_to_surv_model.loc[:,col] = 0

    surv_prediction = survival_model.predict_survival_function(
        data_to_surv_model,
        conditional_after = data_to_surv_model["days_to_churn"].astype(int)
    )
    days_to_churn = surv_prediction.loc[(surv_prediction>=survival_threshold).values].index[-1]
    return {"prediction": prediction, "predicted_days_to_churn": days_to_churn}
