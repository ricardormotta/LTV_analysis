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
# Install and initialize Google Cloud client
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-435.0.1-linux-x86_64.tar.gz
RUN tar -xf google-cloud-cli-435.0.1-linux-x86_64.tar.gz
RUN /google-cloud-sdk/install.sh
ENV PATH="$PATH:/google-cloud-sdk/bin"

EXPOSE 8080

# Expose the port your Kedro application runs on (if needed)
# Command to run your Kedro project
WORKDIR .
ENTRYPOINT ["streamlit", "run", "/prediction_app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]