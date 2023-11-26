"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.14
"""
import pandas as pd
from xgboost import XGBClassifier
import lifelines

import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn import set_config
import lifelines

set_config(transform_output="pandas")

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


def create_column_transformer(cat_cols, num_cols):
    CT = ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
            ("numerical", StandardScaler(), num_cols),
        ]
    )
    return CT

def train_classification_model(X_train, y_train, CT, hyper_parameters):
    xgb = XGBClassifier()
    grid_search = GridSearchCV(xgb, hyper_parameters, n_jobs=-1, verbose=2)
    pipe = Pipeline([("CT", CT), ("model", grid_search)])
    pipe.fit(X_train, y_train)
    return pipe


def train_clustering_model(X_train, CT, hyper_parameters):
    k=hyper_parameters["k"]
    n_splits=hyper_parameters["n_splits"]
    kf = KFold(n_splits=n_splits, shuffle=True)
    kmeans = KMeans(n_clusters=k)
    pipe = Pipeline([("CT", CT), ("model", kmeans)])
    pipe.fit(X_train)
    return pipe