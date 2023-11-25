"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import make_feature_engineering


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=make_feature_engineering,
            inputs="pre_processed_df",
            outputs="features_df",
        )
    ])
