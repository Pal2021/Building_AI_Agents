from dotenv import load_dotenv

load_dotenv()


class SearchService:
    def __init__(self, providers, ranker=None):
        if isinstance(providers, (list, tuple)):
            self.providers = list(providers)
        else:
            self.providers = [providers]
        self.ranker = ranker

    def search_to_string(self, query: str, max_results: int = 3) -> str:
        results = []
        seen_urls = set()

        for provider in self.providers:
            provider_results = provider.execute_search(query, max_results)
            for result in provider_results:
                url = result.get("url", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                result["source"] = provider.__class__.__name__
                results.append(result)

        if self.ranker and results:
            try:
                results = self.ranker.rank(query, results, max_results)
            except Exception as error:
                print(f"[Warning LLM ranking skipped]: {error}")

        if not results:
            return (
                f"# Job Search Results\n\n**Query:** {query}\n\n"
                "No internet search data found.\n"
            )

        formatted_str = (
            "# Job Search Results\n\n"
            f"**Query:** {query}\n\n"
            f"**Sources:** {', '.join(provider.__class__.__name__ for provider in self.providers)}\n\n"
        )
        for idx, item in enumerate(results, 1):
            formatted_str += (
                f"## {idx}. {item['title']}\n\n"
                f"**Source:** {item['source']}\n\n"
                f"**Relevance:** {item.get('relevance_score', 'Not LLM-ranked')}\n\n"
                f"**Link:** [{item['url']}]({item['url']})\n\n"
                f"{item['snippet']}\n\n"
                f"**Reason:** {item.get('relevance_reason', 'Provider result')}\n\n"
            )
        return formatted_str