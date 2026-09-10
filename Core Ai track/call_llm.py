from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def callingLLM():
    endpoint = "https://newaiprashant.services.ai.azure.com/openai/v1"
    
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default"
    )

    client = OpenAI(base_url=endpoint, api_key=token_provider)
    return client


def call_llm(system_prompt, user_prompt, model="gpt-4", on_token=None):
    client = callingLLM()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=on_token is not None,
    )

    if on_token is None:
        return response.choices[0].message.content

    output = []
    for chunk in response:
        if not chunk.choices:
            continue

        token = chunk.choices[0].delta.content or ""
        if token:
            output.append(token)
            on_token(token)
    return "".join(output)