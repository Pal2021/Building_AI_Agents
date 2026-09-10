import json
import os

from app.services.azure_llm import call_llm


class LLMRanker:
    """Scores search candidates against the user's job-search requirements."""

    def __init__(self, model: str):
        self.model = model

    def rank(self, query: str, results: list[dict], max_results: int) -> list[dict]:
        candidates = [
            {
                "id": index,
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("snippet", "")[:1200],
                "source": result.get("source", ""),
            }
            for index, result in enumerate(results)
        ]

        response = call_llm(
            system_prompt=(
                "You are a strict job-search relevance evaluator. "
                "Reject aggregators, expired/listing pages, unrelated roles, "
                "and results without enough evidence. Prefer direct employer "
                "career pages or official ATS job-detail pages. Return JSON only."
            ),
            user_prompt=json.dumps(
                {
                    "query": query,
                    "instructions": {
                        "score": "0-100",
                        "keep_only": "score >= 65",
                        "return": "The best candidates, sorted by score descending, up to the requested limit.",
                    },
                    "candidates": candidates,
                }
            ),
            model=self.model,
            response_format={"type": "json_object"},
        )

        payload = json.loads(response)
        ranked = payload.get("results", [])
        by_id = {index: result for index, result in enumerate(results)}
        final_results = []

        for item in ranked:
            candidate_id = item.get("id")
            if candidate_id not in by_id or item.get("score", 0) < 65:
                continue
            result = dict(by_id[candidate_id])
            result["relevance_score"] = item.get("score")
            result["relevance_reason"] = item.get("reason", "")
            final_results.append(result)
            if len(final_results) == max_results:
                break

        return final_results