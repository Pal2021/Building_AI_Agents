import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI


def calling_llm() -> OpenAI:
    endpoint = os.getenv(
        "AZURE_AI_ENDPOINT",
        "https://newaiprashant.services.ai.azure.com/openai/v1",
    )
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )
    return OpenAI(base_url=endpoint, api_key=token_provider)


def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: str = "gpt-4",
    on_token=None,
    response_format: dict | None = None,
) -> str:
    request = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if response_format:
        request["response_format"] = response_format

    request["stream"] = on_token is not None
    response = calling_llm().chat.completions.create(**request)

    if on_token is None:
        return response.choices[0].message.content or ""

    output = []
    for chunk in response:
        if not chunk.choices:
            continue
        token = chunk.choices[0].delta.content or ""
        if token:
            output.append(token)
            on_token(token)
    return "".join(output)