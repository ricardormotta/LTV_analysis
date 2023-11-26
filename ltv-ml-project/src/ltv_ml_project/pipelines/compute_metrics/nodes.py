"""
This is a boilerplate pipeline 'compute_metrics'
generated using Kedro 0.18.14
"""
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold

import seaborn as sns
import matplotlib.pyplot as plt


def plot_ROC(_pipe, _X, _y, ax, color, dataset_name):
    probs = _pipe.predict_proba(_X)
    preds = probs[:, 1]
    fpr, tpr, threshold = metrics.roc_curve(_y, preds)
    roc_auc = metrics.auc(fpr, tpr)
    # method I: plt
    ax.set_title(f'ROC Curve: {type(_pipe["model"]).__name__}')
    ax.plot(fpr, tpr, color=color, label=f"AUC {dataset_name} = {round(roc_auc, 5)}")
    ax.legend(loc="lower right")
    ax.plot([0, 1], [0, 1], "--", color="black")
    ax.set_xlim([-0.01, 1.01])
    ax.set_ylim([-0.01, 1.01])
    ax.set_ylabel("True Positive Rate")
    ax.set_xlabel("False Positive Rate")
    return ax


def plot_confusion_matrix(_pipe, _X, _y, ax, dataset_name="Test"):
    # Predict labels using the provided model
    _y_pred = _pipe.predict(_X)

    # Generate confusion matrix
    cm = metrics.confusion_matrix(_y, _y_pred)

    # Plotting the confusion matrix using seaborn heatmap
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=_pipe["model"].classes_,
        yticklabels=_pipe["model"].classes_,
        ax=ax,
    )
    ax.set_xlabel("Predicted labels")
    ax.set_ylabel("True labels")
    ax.set_title(f"Confusion Matrix")
    return ax


def plot_ROC_and_confusion_matrix(pipe, X_train, X_test, y_train, y_test):
    palette = sns.color_palette()
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    plot_ROC(pipe, X_test, y_test, ax=axs[0], color=palette[0], dataset_name="Test")
    plot_ROC(pipe, X_train, y_train, ax=axs[0], dataset_name="Train", color=palette[1])

    plot_confusion_matrix(pipe, X_test, y_test, ax=axs[1])
    plt.tight_layout()

    # plt.show()
    plt.close()
    return fig


def plot_elbow_kfold(data, CT, max_clusters=10, n_splits=5):
    kf = KFold(n_splits=n_splits, shuffle=True)
    inertias = []
    data = CT.fit_transform(data)
    for k in range(1, max_clusters + 1):
        fold_inertias = []
        for train_index, _ in kf.split(data):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(data.iloc[train_index])
            fold_inertias.append(kmeans.inertia_)

        inertias.append(np.mean(fold_inertias))

    # Plotting the elbow plot
    sns.set(style="whitegrid")
    fig = plt.figure(figsize=(8, 6))
    plt.plot(range(1, max_clusters + 1), inertias, marker="o")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Average Within-Cluster Sum of Squares (Inertia)")
    plt.title("Elbow Method using K-Fold Cross Validation")
    plt.axvline(6, linestyle="--")
    plt.xticks(np.arange(1, max_clusters + 1))
    return fig


def get_top_cluster_features(data, _pipe, top_n_features):
    # Assign cluster labels to each data point
    labels = _pipe["model"].labels_
    k = len(np.unique(labels))
    data["Cluster"] = labels
    data = _pipe["CT"].transform(data)

    # Calculate centroids for each cluster
    centroids = _pipe["model"].cluster_centers_

    # Get feature importances for each cluster
    cluster_features = {}
    for cluster in range(k):
        centroid = centroids[cluster]
        abs_centroid = np.abs(centroid)  # Take absolute values for importance

        # Sort indices by importance and get top_n
        top_indices = np.argsort(abs_centroid)[::-1][:top_n_features]

        # Get feature names and importance values
        feature_names = _pipe[0].get_feature_names_out()[top_indices]
        feature_importance = centroid[top_indices]

        cluster_features[cluster] = pd.DataFrame(
            {"Features": feature_names, "Importance": feature_importance}
        )

    return cluster_features
