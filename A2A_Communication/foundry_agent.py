class FoundryAgent():
    """This class will contain helper functions for interacting with our Foundry Agent"""

    def __init__(self, project_client, agent_name):
        self.project_client = project_client
        self.agent_name = agent_name

    async def invoke_agent(self, user_query: str) -> str:
        openai_client = self.project_client.get_openai_client()

        conversation = openai_client.conversations.create()

        response =  openai_client.responses.create(
            conversation=conversation.id,
            extra_body={
                "agent": {
                    "name": self.agent_name,
                    "type": "agent_reference"
                }
            },
            input=user_query
        )

        return response.output_text