from azure.ai.projects.models import PromptAgentDefinition

from foundry_client import create_project_client


agent_name = "batman-agent"
model_deployment_name = "gpt-5"


async def create_agent():

    project_client = create_project_client()

    agent = project_client.agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(
            model=model_deployment_name,
            instructions="You are Batman. You are a helpful assistant."
        ),
    )

    return agent

    project_client = create_project_client()

    agent = await project_client.agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(
            model=model_deployment_name,
            instructions="You are Batman. You are a helpful assistant."
        ),
    )

    return agent