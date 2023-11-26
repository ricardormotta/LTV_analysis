import os
import sys
import pandas as pd
import streamlit as st

sys.path.append("..")
from start_kedro_session import get_kedro_catalog
from predict_utils import predict_from_survival_model

catalog = get_kedro_catalog()
classifier = catalog.load("trained_classifier_pipeline")
survival_model = catalog.load("survival_model")
survival_threshold = catalog.load("params:survival_threshold")
train_cols_surv_model = survival_model.variance_matrix_.columns
cat_features = catalog.load("params:cat_cols")


# Streamlit app begins here
st.title('LTV Analysis')
st.text('Author: Ricardo Motta')

st.markdown('''
    This app intents to show you the results of the LTV Analysis developed by the Author.

    The source code can be found at [https://github.com/ricardormotta/LTV_analysis](https://github.com/ricardormotta/LTV_analysis)
            
    There are 4 subpages in this app, which can be navigated through the side menu:
    - EDA: Showing the exploratory data analysis
    - Classification Model: Showing the trained classification model used on churn analysis
    - Survival Model: Showing the survival analysis to predict the time to churn
    - Segmentation Model: Showing the segmentation model to predict better cross-selling opportunities

    All those models can be also accessed via an POST request in an API. The documentation of the API can be seen at:
    [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
    
    You can also run predictions using the interface below. Try it out!
''')
# Sidebar for user input
st.header('Model testing')
channel = st.selectbox('Channel', ('channel_a', 'channel_b'))
age = st.selectbox("Age group", ('18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55+'))
op_system = st.selectbox("Operating system", ("iOS","Android",))
base_product = st.selectbox("Base Product", ("product_a", "product_b", "product_c"))
base_commission = st.number_input("Base commission", value=0)
client_since_days = st.number_input("Cliente since (days)", value=0)
product_x = st.select_slider("Number of purchases of Product X", range(0,6,1), value=0)
product_y = st.select_slider("Number of purchases of Product Y", range(0,6,1), value=0)
is_xs = False
# Add more input features as needed
inputs = {
    "channel": [channel],
    "age_bucket": [age],
    "operating_system": [op_system],
    "product": [base_product],
    "commission": [base_commission],
    "product_x": [product_x],
    "product_y": [product_y],
    "is_xs": [is_xs],
    "days_to_churn": [client_since_days],
}
# Button to trigger prediction
if st.button('Run Prediction'):
    if product_x+product_y>0:
        is_xs=True
    data = pd.DataFrame.from_dict(inputs, orient="index").T
    print(data.head())
    input_features = []  # Gather input features
    proba = classifier.predict_proba(data)[0,1]
    prediction = classifier.predict(data)
    days_to_churn = predict_from_survival_model(data, survival_model, cat_features, survival_threshold)
    will_churn = "Yes" if bool(prediction[0]) else "No"
    st.header("Models' outputs:")
    st.write(f"\tWill this cliente churn? {will_churn}")
    st.write(f"\tPredicted probability of churn: {proba}")
    st.write(f"\tPredicted days to churn: {days_to_churn}")
