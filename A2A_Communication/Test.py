import asyncio

from a2a_client import get_agent_card, send_message


async def main():

    agent_card = await get_agent_card()

    print("Agent Card received!")

    await send_message(agent_card)


asyncio.run(main())