import uvicorn

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from a2a.utils import new_agent_text_message


class BatmanAgentExecutor(AgentExecutor):

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        user_input = context.get_user_input()

        response = f"Batman received: {user_input}"

        await event_queue.enqueue_event(
            new_agent_text_message(response)
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        raise Exception("Cancel not supported")


skill = AgentSkill(
    id="batman",
    name="Batman Agent",
    description="A simple Batman A2A agent",
    tags=["batman", "superhero"],
    examples=["Who are you?", "What can you do?"],
)

agent_card = AgentCard(
    name="Batman Agent",
    description="A simple Batman A2A agent",
    url="http://localhost:8080",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(
        streaming=False,
    ),
    skills=[skill],
)

request_handler = DefaultRequestHandler(
    agent_executor=BatmanAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

if __name__ == "__main__":
    uvicorn.run(
        server.build(),
        host="localhost",
        port=8080,
    )