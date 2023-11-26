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
    train_classification_model,
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
                    "params:target",
                ],
                outputs=["X", "y"],
            ),
            node(
                func=split_train_test,
                inputs=["X", "y", "params:train_test_ratio", "params:SEED"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
            ),
            node(
                func=train_survival_model,
                inputs=["X", "y", "params:cat_cols"],
                outputs="survival_model",
            ),
            node(
                func=create_column_transformer,
                inputs=[
                    "params:cat_cols",
                    "params:num_cols",
                ],
                outputs="CT"
            ),
            node(
                func=train_classification_model,
                inputs=[
                    "X_train",
                    "y_train",
                    "CT",
                    "params:xgb_parameters",
                ],
                outputs="trained_classifier_pipeline",
            ),
            node(
                func=train_clustering_model,
                inputs=[
                    "X_train",
                    "CT",
                    "params:kfold_parameters"
                ],
                outputs="trained_kfolds"
            )
        ]
    )
