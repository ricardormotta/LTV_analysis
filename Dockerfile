FROM python:3.10

# Create and set the working directory in the container
# run git clone https://github.com/ricardormotta/LTV_analysis.git .
# Copy the requirements file and install dependencies
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# Copy the entire Kedro project into the container
COPY . .
# WORKDIR ./ltv-ml-project
# RUN kedro run
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN mkdir -p /usr/local/gcloud
RUN tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz
RUN /usr/local/gcloud/google-cloud-sdk/install.sh
RUN /usr/local/gcloud/google-cloud-sdk/bin/gcloud auth activate-service-account ltv-analysis@ltv-analysis-406313.iam.gserviceaccount.com --key-file=/ltv-ml-project/conf/local/ltv-analysis-406313-7bac47acc42e.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/ltv-ml-project/conf/local/ltv-analysis-406313-7bac47acc42e.json

EXPOSE 8080

# Expose the port your Kedro application runs on (if needed)
# Command to run your Kedro project
ENV GOOGLE_APPLICATION_CREDENTIALS=./ltv-ml-project/conf/local/ltv-analysis-406313-7bac47acc42e.json
WORKDIR .
ENTRYPOINT ["streamlit", "run", "/prediction_app/streamlit/main.py", "--server.port=8080", "--server.address=0.0.0.0"]