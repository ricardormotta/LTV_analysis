import pandas as pd 

def predict_from_survival_model(data, survival_model, cat_features, survival_threshold):
    train_cols_surv_model = survival_model.variance_matrix_.columns

    data_to_surv_model = pd.get_dummies(data, columns=cat_features)
    missing_cols = train_cols_surv_model[~train_cols_surv_model.isin(data_to_surv_model.columns)]
    for col in missing_cols:
        data_to_surv_model.loc[:,col] = 0

    surv_prediction = survival_model.predict_survival_function(
        data_to_surv_model,
        conditional_after = data_to_surv_model["days_to_churn"].astype(int)
    )
    days_to_churn = surv_prediction.loc[(surv_prediction>=survival_threshold).values].index[-1]
    return days_to_churn
