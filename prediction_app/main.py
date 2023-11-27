import os
import sys
import pandas as pd
import streamlit as st

sys.path.append("..")
from start_kedro_session import get_kedro_catalog, get_kedro_project_path
from predict_utils import predict_from_survival_model
from secret_manager_helper import get_secret_as_json

project_id = "840195815299"
secret_id = "ltv_service_account"
kedro_project_path = get_kedro_project_path()
st.title("LTV Analysis")

token_path = os.path.join(kedro_project_path, "conf", "local", "gcp_token.json")
token_saved = get_secret_as_json(project_id, secret_id, token_path)

catalog = get_kedro_catalog()
classifier = catalog.load("trained_classifier_pipeline")
regressor = catalog.load("trained_ltv_pipeline")
survival_model = catalog.load("survival_model")
survival_threshold = catalog.load("params:survival_threshold")
train_cols_surv_model = survival_model.variance_matrix_.columns
cat_features = catalog.load("params:cat_cols")
clusterer = catalog.load("trained_kfolds")
cluster_feature_importances = catalog.load("cluster_centroids")


# Streamlit app begins here
st.text("Author: Ricardo Motta")
st.text("https://linkedin.com/in/ricardormotta")

st.markdown(
    """
    This project focuses on Lifetime Value (LTV) analysis, encompassing churn analysis, LTV prediction, and customer segmentation.

    The source code can be found at [https://github.com/ricardormotta/LTV_analysis](https://github.com/ricardormotta/LTV_analysis)
            
    You can run predictions using the interface below. Try it out!
"""
)
# Sidebar for user input
st.header("Model testing")
channel = st.selectbox("Channel", ("channel_a", "channel_b"))
age = st.selectbox(
    "Age group", ("18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55+")
)
op_system = st.selectbox(
    "Operating system",
    (
        "iOS",
        "Android",
    ),
)
base_product = st.selectbox("Base Product", ("product_a", "product_b", "product_c"))
base_commission = st.number_input("Base commission", value=0)
xs_commission = st.number_input("Cross Selling commission", value=0)
client_since_days = st.number_input("Client since (days)", value=0)
product_x = st.select_slider(
    "Number of purchases of Product X", range(0, 6, 1), value=0
)
product_y = st.select_slider(
    "Number of purchases of Product Y", range(0, 6, 1), value=0
)
is_xs = False
# Add more input features as needed
inputs = {
    "channel": [channel],
    "age_bucket": [age],
    "operating_system": [op_system],
    "product": [base_product],
    "commission_base": [base_commission],
    "commission_xs": [xs_commission],
    "product_x": [product_x],
    "product_y": [product_y],
    "is_xs": [is_xs],
    "days_to_churn": [client_since_days],
}
# Button to trigger prediction
if st.button("Run Prediction"):
    if product_x + product_y > 0:
        is_xs = True
    data = pd.DataFrame.from_dict(inputs, orient="index").T
    print(data.head())
    input_features = []  # Gather input features
    proba = classifier.predict_proba(data)[0, 1]
    prediction = classifier.predict(data)
    days_to_churn = predict_from_survival_model(
        data, survival_model, cat_features, survival_threshold
    )
    cluster = clusterer.predict(data)[0]
    cluster_features = cluster_feature_importances[cluster]
    data.loc[:,"days_to_churn"] = 0
    predicted_months = regressor.predict(data)[0]

    will_churn = "Yes" if bool(prediction[0]) else "No"
    st.header("Models' outputs:")
    st.write(f"\tWill this client churn? {will_churn}")
    st.write(f"\tPredicted probability of churn: {round(proba,5)}")
    st.write(f"\tPredicted days to churn according to the survival model: {round(days_to_churn,3)}")
    st.write(f"\tPredicted retention months according to the LTV model: {round(predicted_months,3)}")
    st.write(f"\tThis client was assigned to cluster {cluster}")
    st.write(f"\tThis cluster has the following most important features:")
    st.dataframe(cluster_features)
