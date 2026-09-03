from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


# PROJECT_ENDPOINT = "YOUR_FOUNDRY_PROJECT_ENDPOINT"

PROJECT_ENDPOINT = "https://newaiprashant.services.ai.azure.com/api/projects/newaiprashantproject"
def create_project_client():
    credential = DefaultAzureCredential()

    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential
    )

    return project_client