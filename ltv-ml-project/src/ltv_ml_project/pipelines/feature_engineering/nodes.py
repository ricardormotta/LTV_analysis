"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.14
"""
import numpy as np
import pandas as pd

def make_feature_engineering(df):
    df.loc[:,["commission_xs", "product_x",  "product_y"]] = df.loc[:,["commission_xs", "product_x",  "product_y"]].fillna(0)

    df.loc[:, "is_xs"] = np.where(
        (df["product_x"] + df["product_y"]) > 0,
        1,
        0
    )
    datetime_cols = ["customer_churned_at", "customer_started_at"]
    for col in datetime_cols:
        df.loc[:, col] = pd.to_datetime(df.loc[:,col], errors="coerce")

    df.loc[:,"is_churn"] = ~df["customer_churned_at"].isna()
    df.loc[df["is_churn"], "days_to_churn"] = (
        pd.to_datetime(df.loc[df["is_churn"], "customer_churned_at"]).subtract(
            pd.to_datetime(df.loc[df["is_churn"] ,"customer_started_at"])
        ).dt.days
    )
    actual_date = max(df["customer_churned_at"].dropna().max(), df["customer_started_at"].dropna().max())
    df.loc[df["days_to_churn"]<0, "days_to_churn"] = 0
    df.loc[~df["is_churn"], "days_to_churn"] = (actual_date - pd.to_datetime(df.loc[~df["is_churn"], "customer_started_at"])).dt.days
    return df
    