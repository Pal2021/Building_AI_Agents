from ddgs import DDGS

from app.providers.base import BaseSearchProvider


class DuckDuckGoProvider(BaseSearchProvider):
    """Uses DuckDuckGo (Free, powered behind-the-scenes by Bing)"""

    blocked_domains = (
        "linkedin.com",
        "indeed.com",
        "glassdoor.com",
        "naukri.com",
        "foundit.in",
        "monster.com",
        "ziprecruiter.com",
        "simplyhired.com",
        "wellfound.com",
        "cutshort.io",
        "dice.com",
    )

    def execute_search(self, query: str, max_results: int) -> list[dict]:
        try:
            with DDGS() as ddgs:
                raw_data = ddgs.text(
                    query,
                    max_results=max_results * 4,
                    timelimit="d",
                )

                results = []
                seen_urls = set()
                for result in raw_data:
                    url = result.get("href", "")
                    url_lower = url.lower()
                    if not url or url in seen_urls:
                        continue
                    if any(domain in url_lower for domain in self.blocked_domains):
                        continue
                    if not any(
                        marker in url_lower
                        for marker in ("career", "job", "join-us", "joinus", "work-with-us")
                    ):
                        continue

                    seen_urls.add(url)
                    results.append(
                        {
                            "title": result.get("title", "No title"),
                            "url": url,
                            "snippet": result.get("body", ""),
                        }
                    )
                    if len(results) == max_results:
                        break

                return results
        except Exception as e:
            print(f"[Error DDG]: {e}")
            return []