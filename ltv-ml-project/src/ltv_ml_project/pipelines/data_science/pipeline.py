"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    split_X_y,
    split_train_test,
    create_column_transformer,
    train_survival_model,
    train_xgb,
    train_clustering_model,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_X_y,
                inputs=[
                    "features_df",
                    "params:cat_cols",
                    "params:num_cols",
                    "params:ohe_cols",
                    "params:target_churn",
                ],
                outputs=["X", "y_churn"],
            ),
            node(
                func=split_train_test,
                inputs=["X", "y_churn", "params:train_test_ratio", "params:SEED"],
                outputs=["X_train", "X_test", "y_train_churn", "y_test_churn"],
            ),
            node(
                func=train_survival_model,
                inputs=["X", "y_churn", "params:cat_cols"],
                outputs="survival_model",
            ),
            node(
                func=create_column_transformer,
                inputs=[
                    "params:cat_cols",
                    "params:num_cols",
                ],
                outputs="CT",
            ),
            node(
                func=train_xgb,
                inputs=[
                    "X_train",
                    "y_train_churn",
                    "CT",
                    "params:xgb_parameters",
                    "params:problem_type_classification",
                ],
                outputs="trained_classifier_pipeline",
            ),
            node(
                func=split_X_y,
                inputs=[
                    "features_df",
                    "params:cat_cols",
                    "params:num_cols",
                    "params:ohe_cols",
                    "params:target_ltv",
                ],
                outputs=["X_ltv", "y_ltv"],
            ),
            node(
                func=split_train_test,
                inputs=["X", "y_ltv", "params:train_test_ratio", "params:SEED"],
                outputs=["X_train_ltv", "X_test_ltv", "y_train_ltv", "y_test_ltv"],
            ),
            node(
                func=train_xgb,
                inputs=[
                    "X_train",
                    "y_train_ltv",
                    "CT",
                    "params:xgb_parameters",
                    "params:problem_type_regression",
                ],
                outputs="trained_ltv_pipeline",
            ),
            node(
                func=train_clustering_model,
                inputs=["X_train", "CT", "params:kfold_parameters"],
                outputs="trained_kfolds",
            ),
        ]
    )
