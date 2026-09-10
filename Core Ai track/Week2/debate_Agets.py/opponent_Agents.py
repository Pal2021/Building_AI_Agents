from call_llm import call_llm

opponent_model = "gpt-5"


def opponent_agent(topic, opponent_memory, on_token=None):
    system_prompt = """
    You are the OPPONENT in a debate.

    Your job is to argue AGAINST the given topic.

    Rules:
    - Directly answer the defender's latest argument.
    - Identify weaknesses and give logical counterarguments with examples.
    - Challenge assumptions.
    - Do not attack the opponent personally.
    - End with exactly one short counter-question for the defender.
    - Keep the response under 100 words.
    """

    return call_llm(
        model=opponent_model,
        system_prompt=system_prompt,
        user_prompt=(
            f"Debate topic: {topic}\n"
            f"Defender's latest argument: {opponent_memory[-1] if opponent_memory else 'No previous argument. Give your opening case.'}\n"
            f"Previous defender arguments: {opponent_memory}\n"
            "Argue against the topic, directly rebut the latest argument, and end with one counter-question."
        ),
        on_token=on_token,
    )