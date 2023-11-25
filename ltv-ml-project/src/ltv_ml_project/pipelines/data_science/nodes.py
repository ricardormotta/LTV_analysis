"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.14
"""
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier
import lifelines

import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import lifelines


def split_X_y(
    df,
    cat_cols,
    num_cols,
    ohe_cols,
    target,
):
    features = [*cat_cols, *num_cols, *ohe_cols]

    X = df[features]
    y = df[target]
    return X, y


def split_train_test(
    X,
    y,
    train_test_ratio,
    SEED,
):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=train_test_ratio, random_state=SEED
    )
    return X_train, X_test, y_train, y_test


def train_survival_model(X, y, cat_cols):
    data = pd.concat([X, y], axis=1)
    data = pd.get_dummies(data, columns=cat_cols, drop_first=False)
    cph = lifelines.CoxPHFitter(penalizer=0.0001)
    cph.fit(data, duration_col="days_to_churn", event_col="is_churn")
    return cph


def train_classification_model(X_train, y_train, cat_cols, num_cols, hyper_parameters):
    xgb = XGBClassifier()

    CT = ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("numerical", StandardScaler(), num_cols),
        ]
    )
    grid_search = GridSearchCV(xgb, hyper_parameters, n_jobs=-1, verbose=2)
    pipe = Pipeline([("CT", CT), ("model", grid_search)])
    pipe.fit(X_train, y_train)
    return pipe
