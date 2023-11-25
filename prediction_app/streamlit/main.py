import os
import streamlit as st
import pickle  # Or any library you use to load your model
from typing import List

from ..start_kedro_session import get_kedro_catalog
from ..predict_utils import predict_from_survival_model

catalog = get_kedro_catalog()
classifier = catalog.load("trained_classifier_pipeline")
survival_model = catalog.load("survival_model")
survival_threshold = catalog.load("params:survival_threshold")
train_cols_surv_model = survival_model.variance_matrix_.columns
cat_features = catalog.load("params:cat_cols")


# Streamlit app begins here
st.title('Machine Learning Model Prediction App')

# Sidebar for user input
st.sidebar.title('Input Features')
feature1 = st.sidebar.number_input('Feature 1', value=0.0)
feature2 = st.sidebar.number_input('Feature 2', value=0.0)
# Add more input features as needed

# Button to trigger prediction
if st.sidebar.button('Run Prediction'):
    input_features = [feature1, feature2]  # Gather input features
    prediction = classifier.predict(input_features)  # Make prediction

    st.write(f"Prediction: {prediction}")
