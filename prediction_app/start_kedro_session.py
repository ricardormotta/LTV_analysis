import os 

from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
# Create a Kedro context

def start_kedro_context():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kedro_project_name = "ltv-ml-project"
    project_path = os.path.join(base_dir, kedro_project_name)
    bootstrap_project(project_path)
    session = KedroSession.create(
        package_name=kedro_project_name,
        project_path=project_path,
    )

    # Load the Kedro project context
    return session

def get_kedro_catalog():
    session = start_kedro_context()
    context = session.load_context()
    return context.catalog
