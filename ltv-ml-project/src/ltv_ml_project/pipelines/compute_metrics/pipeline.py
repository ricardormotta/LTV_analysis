"""
This is a boilerplate pipeline 'compute_metrics'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import plot_ROC_and_confusion_matrix, plot_elbow_kfold, get_top_cluster_features


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=plot_ROC_and_confusion_matrix,
            inputs=["trained_classifier_pipeline", "X_train", "X_test", "y_train", "y_test"],
            outputs="classification_metrics"
        ),
        node(
            func=plot_elbow_kfold,
            inputs=["X_train", "CT", "params:max_clusters", "params:n_splits"],
            outputs="elbow_curve"
        ),
        node(
            func=get_top_cluster_features,
            inputs=["X_train", "trained_kfolds", "params:top_n_features"],
            outputs="cluster_centroids"
        )
    ])
