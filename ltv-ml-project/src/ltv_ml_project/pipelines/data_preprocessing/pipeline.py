"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import pre_process_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=pre_process_data,
            inputs=["base", "xs", "params:datetime_cols"],
            outputs="pre_processed_df"
        )
    ])
