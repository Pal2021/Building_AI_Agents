import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from defender_Agents import defender_agent
from defender_Agents import defender_model
from opponent_Agents import opponent_agent
from opponent_Agents import opponent_model
from call_llm import call_llm


def orchestrator_Agets(topic, rounds=3):
    """Run a debate and return both sides' arguments and the judge's verdict."""
    if not topic or not topic.strip():
        raise ValueError("topic must not be empty")
    if not isinstance(rounds, int) or rounds < 1:
        raise ValueError("rounds must be a positive integer")

    defender_memory = []
    opponent_memory = []
    debate_rounds = []
    print(f"# Debate: {topic}\n\nRounds: {rounds}\n")
    for round_number in range(1, rounds + 1):
        print(f"## Round {round_number}\n\n**Defender ({defender_model}):** ", end="", flush=True)
        defender_argument = defender_agent(
            topic,
            opponent_memory,
            on_token=lambda token: print(token, end="", flush=True),
        )
        defender_memory.append(defender_argument)
        print("\n")

        print(f"**Opponent ({opponent_model}):** ", end="", flush=True)
        opponent_argument = opponent_agent(
            topic,
            defender_memory,
            on_token=lambda token: print(token, end="", flush=True),
        )
        opponent_memory.append(opponent_argument)
        print("\n")
        debate_rounds.append(
            {
                "round": round_number,
                "defender": defender_argument,
                "opponent": opponent_argument,
            }
        )

    judge_prompt = f"""
You are the judge in a debate.

Topic: {topic}

Round-by-round debate transcript:
{debate_rounds}

Evaluate every round. For each round, compare rebuttal quality, evidence,
relevance, and whether the agent answered the latest argument and asked a useful
counter-question. Then evaluate overall performance across all rounds.
Return exactly:
Round scores: R1 [Defender/Opponent/Tie], R2 [Defender/Opponent/Tie], ...
Overall winner: [Defender/Opponent]
Winning model: [model name]
Reason: [one short sentence]
"""
    print("## Final Verdict\n\n**Judge (gpt-5.6-sol):** ", end="", flush=True)
    verdict = call_llm(
        model="gpt-5.6-sol",
        system_prompt="Judge fairly. Return exactly: Winner: [side]. Reason: [one short sentence].",
        user_prompt=judge_prompt,
        on_token=lambda token: print(token, end="", flush=True),
    )
    print("\n")

    return {
        "topic": topic,
        "defender_arguments": defender_memory,
        "opponent_arguments": opponent_memory,
        "rounds": debate_rounds,
        "verdict": verdict,
    }


if __name__ == "__main__":
    orchestrator_Agets(
        "Is AI a threat to humanity?",
        rounds=3,
    )



