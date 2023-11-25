"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.14
"""
import numpy as np
import pandas as pd


def pre_process_data(base, xs, datetime_cols):

    base.loc[:, "operating_system"] = base["operating_system"].replace({"iPadOS": "iOS", "iPhone OS": "iOS"})

    xs = pd.merge(
        xs,
        pd.get_dummies(xs["product"]),
        left_index=True,
        right_index=True,
    )

    grouped_xs = xs.groupby("user_id").sum()[["commission", "product_x", "product_y"]].reset_index()

    df = pd.merge(
        base,
        grouped_xs,
        on="user_id",
        how="left",
        suffixes=["_base", "_xs"]
    )
    for col in datetime_cols:
        df.loc[:, col] = pd.to_datetime(df[col], errors="coerce", utc=False)

    return df