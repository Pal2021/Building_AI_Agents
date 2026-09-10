import os
from pathlib import Path

from dotenv import load_dotenv

from app.providers.company_careers import FrequentlyHiringCompaniesProvider
from app.providers.duckduckgo import DuckDuckGoProvider
from app.providers.exa import ExaProvider
from app.providers.tavily import TavilyProvider
from app.services.llm_ranker import LLMRanker
from app.services.search_service import SearchService

load_dotenv()


def main():
    search_query = (
        'java developer job in India today for maximum 2 years of experience'
    )

    providers = [
        DuckDuckGoProvider(),
        FrequentlyHiringCompaniesProvider(),
    ]

    if os.getenv("EXA_API_KEY"):
        providers.append(ExaProvider())

    if os.getenv("TAVILY_API_KEY"):
        providers.append(TavilyProvider())

    azure_model = os.getenv("AZURE_AI_MODEL")
    ranker = LLMRanker(azure_model) if azure_model else None
    search_engine = SearchService(providers, ranker=ranker)

    search_prompt_context = search_engine.search_to_string(
        search_query,
        max_results=10,
    )

    project_root = Path(__file__).resolve().parent.parent
    output_file = project_root / "search_results_1.md"
    file_number = 1
    while output_file.exists():
        file_number += 1
        output_file = project_root / f"search_results_{file_number}.md"

    output_file.write_text(search_prompt_context, encoding="utf-8")
    print(f"Search results saved to: {output_file}")


if __name__ == "__main__":
    main()