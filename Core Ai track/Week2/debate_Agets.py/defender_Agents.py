from call_llm import call_llm

defender_model = "gpt-5-mini"


def defender_agent(topic, opponent_memory, on_token=None):
    system_prompt = """
    You are the DEFENDER in a debate.

    Your job is to argue FOR the given topic.

    Rules:
    - Directly answer the opponent's latest argument.
    - Give strong logical counterarguments and examples.
    - Do not attack the opponent personally.
    - Focus on facts and reasoning.
    - End with exactly one short counter-question for the opponent.
    - Keep the response under 100 words.
    """

    return call_llm(
        model="gpt-5-mini",
        system_prompt=system_prompt,
        user_prompt=(
            f"Debate topic: {topic}\n"
            f"Opponent's latest argument: {opponent_memory[-1] if opponent_memory else 'No previous argument. Give your opening case.'}\n"
            f"Previous opponent arguments: {opponent_memory}\n"
            "Defend the topic, directly rebut the latest argument, and end with one counter-question."
        ),
        on_token=on_token,
    )
