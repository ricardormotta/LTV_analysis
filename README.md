# LTV Analysis 💸

## Project Overview

This project, developed by [Ricardo Raspini Motta](linkedin.com/in/ricardormotta), focuses on Lifetime Value (LTV) analysis, encompassing churn analysis, LTV prediction, and customer segmentation.

The project includes:
- ML Orchestration using Kedro
- CI/CD using Cloud Build in Google Cloud Platform
- A Streamlit App to run predictions interactively


## Project Structure

The directory structure shows two main folders:
* `ltv-ml-project`: Contains the whole data pipeline, which consists of a kedro project. It also include the notebooks used in the data exploration and analysis. Read more in [here](https://docs.kedro.org/en/0.18.3/faq/architecture_overview.html)
* `prediction_app`: Contains the code to deploy the models in a Streamlit web app, that can enable end-users to run predictions with different inputs.   The app is being deployed [here](https://ltv-analysis-66dlatsw4q-uc.a.run.app/). 


```
.
├── docs
├── ltv-ml-project
│   ├── conf
│   │   ├── base
│   │   └── local
│   ├── data
│   │   ├── 01_raw
│   │   ├── 02_intermediate
│   │   ├── 03_feature
│   │   ├── 03_primary
│   │   ├── 04_feature
│   │   ├── 04_model_input
│   │   ├── 05_model_input
│   │   ├── 06_models
│   │   ├── 07_model_output
│   │   └── 08_reporting
│   ├── docs
│   │   └── source
│   ├── notebooks
│   └── src
│       ├── ltv_ml_project
│       │   └── pipelines
│       │       ├── compute_metrics
│       │       ├── data_preprocessing
│       │       ├── data_science
│       │       └── feature_engineering
│       └── tests
│           └── pipelines
│               ├── compute_metrics
│               ├── data_preprocessing
│               ├── data_science
│               └── feature_engineering
└── prediction_app
```


The sub-folders in `ltv-ml-project` follow the kedro template structure. The more important are:
* conf:
    * Here are the data paths and parameters declared.
    * The `catalog.yml` describes the data sources.
    * The `parameters.yml` describes the pipeline parameters.
* data:
    * This folder is used locally to store data.
* notebooks:
    * Contains the notebooks used in the experiments
* src:
    * Contains the code itself.
    * The code is splitted into different pipelines: `compute_metrics`, `data_preprocessing`, `data_science`, `feature_engineering`. 
    * Inside the subfolder of each pipeline (`src/ltv_ml_project/data_science`, for example), there are the `nodes.py` and `pipeline.py`
    * The `nodes.py` files contain the functions that do the processing in the data
    * The `pipeline.py` files link those nodes with the data sources and parameters declared in the `catalog.yml` and `parameters.yml`

The orchestration is then made by kedro itself.

## Machine Learning Pipeline

The machine learning pipeline was orchestrated using Kedro. The codebase for the pipeline is housed in the `ltv-ml-project` folder. Below is how the pipeline look like:

![Pipeline Screenshot](docs/kedro_viz.png)

To run this visualization, run the command `kedro viz` when inside the folder `ltv-ml-project`. 

This pipeline orchestrate the whole data science code. It includes the data pre-processing, feature engineering, the training of the models and the calculation of the metrics. All data is being managed by the catalog structure, and the linkage between the datasources and the code can be seen in `conf/base/catalog.yml`. 

All data is being saved on the Google Cloud Storage. The training of the models is being run locally, but in the future the plan is to set up a VM to do that.


## Prediction App

A prediction app has been developed using Streamlit for user-friendly interaction. Access the app [here](https://ltv-analysis-66dlatsw4q-uc.a.run.app/).

A screenshot of the app:
![Streamlit](docs/streamlit.png)

To run the app locally, run in the project root directory:
```console
streamlit run /prediction_app/main.py
```

The app should start locally. The same command can be seen in the end of the `Dockerfile`.

## Cloud usage

The cloud provider for this project is the Google Cloud Platform. Currently the app is being deployed to a Cloud Run instance (read more [here](https://cloud.google.com/run?hl=en)). The CI/CD pipeline uses Cloud Build (see `cloudbuild.yaml` file, and read more [here](https://cloud.google.com/build?hl=en)). Every commit in the main branch re-starts the deployment of the model. Next features will include the training of the model in a [Compute Engine](https://cloud.google.com/compute?hl=en) virtual machine. All data and models are being saved in the [Cloud Storage](https://cloud.google.com/storage?hl=en), and the secrets are being managed by the [Secret Manager](https://cloud.google.com/secret-manager).

## Exploratory Data Analysis (EDA)

The exploratory data analysis was conducted in Jupyter Notebooks, available in the `ltv-ml-project/notebooks` directory. There are also notebooks using when developing the models.

## Usage

To replicate this project locally, follow these steps:

1. Clone the repository:

```console
git clone https://github.com/your-username/ltv-analysis-project.git
```

2. Set up the environment:

```console 
pip install -r requirements.txt
```

You will also need the tables `base.csv` and `xs` on the following directory:
`/home/ricardormotta/projects/LTV_analysis/ltv-ml-project/data/01_raw`.

3. Navigate to the project directory:

```console 
cd ltv-analysis-project
```

4. Run the ML pipeline.

```console 
kedro run --env=local
```

You can also here visualize the pipeline with:

```console 
kedro viz --env=local
```

5. Initiate the prediction app:

Navigate back to the root directory and then run:

```console
streamlit run /prediction_app/main.py
```

6. Set up your cloud environment.

This project runs in the Google Cloud Platform, and the CI/CD files can be seen at the `cloudbuild.yaml` and `dockerfile`. Those are being used to deploy this project. You can set up your own project in the cloud and use them as example.


7.  *Extra*: Explore the notebooks in `ltv-ml-project/notebooks` for detailed analysis.

## Contributors

- Ricardo Raspini Motta ([LinkedIn](https://linkedin.com/in/ricardormotta))

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).