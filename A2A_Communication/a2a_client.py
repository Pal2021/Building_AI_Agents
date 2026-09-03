import httpx

from a2a.client.card_resolver import A2ACardResolver
from a2a.types import AgentCard


base_url = "http://localhost:8080"

from uuid import uuid4

from a2a.client import A2AClient
from a2a.types import MessageSendParams, SendMessageRequest


async def send_message_to_agent(agent_card):

    async with httpx.AsyncClient(timeout=60.0) as httpx_client:

        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=agent_card
        )

        request = create_text_message_object(
            content="How is Gotham City doing today?"
        )

        async for response in client.send_message(request):
            task, _ = response
            print(get_message_text(task.artifacts[-1]))

async def get_agent_card():

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=10.0,
            read=60.0,
            write=10.0,
            pool=10.0,
        )
    ) as httpx_client:

        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url
        )

        final_agent_card_to_use: AgentCard | None = None

        try:
            _public_card = await resolver.get_agent_card()

            final_agent_card_to_use = _public_card

        except Exception as e:
            print(
                f"Critical error fetching public agent card: {e}",
                exc_info=True
            )
            raise RuntimeError(
                "Failed to fetch the public agent card. Cannot continue."
            ) from e

        return final_agent_card_to_use

from uuid import uuid4

from a2a.client import A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
)


async def send_message(agent_card):

    async with httpx.AsyncClient(timeout=60.0) as httpx_client:

        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=agent_card
        )

        message = {
            "message_id": uuid4().hex,
            "role": "user",
            "parts": [
                {
                    "kind": "text",
                    "text": "Hello Batman, who are you?"
                }
            ],
        }

        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message=message
            )
        )

        response = await client.send_message(request)

        print("Response received!")
        print(response)