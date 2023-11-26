"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from ltv_ml_project.pipelines.data_preprocessing import (
    create_pipeline as data_preprocessing,
)
from ltv_ml_project.pipelines.feature_engineering import (
    create_pipeline as feature_engineering,
)
from ltv_ml_project.pipelines.data_science import create_pipeline as data_science

from ltv_ml_project.pipelines.compute_metrics import create_pipeline as compute_metrics


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
