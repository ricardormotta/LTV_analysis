
from google.cloud import secretmanager
import json
from start_kedro_session import get_kedro_project_path

def get_secret_as_json(project_id, secret_id, saving_path):
    # Initialize the Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the secret nameprojects
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/1"

    # Access the latest version of the secret
    response = client.access_secret_version(name=secret_name)

    # Get the payload data
    payload = response.payload.data.decode("UTF-8")

    # Convert the payload to a Python dictionary (assuming it's in JSON format)
    secret_data = json.loads(payload)

    # Save the secret as a JSON file
    with open(saving_path, 'w') as json_file:
        json.dump(secret_data, json_file, indent=4)
    
    return f"Secret saved as '{saving_path}'"
    

