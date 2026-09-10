from abc import ABC, abstractmethod


class BaseSearchProvider(ABC):
    """
    Abstract interface. Every new search engine we add in the future 
    MUST follow this exact structural blueprint.
    """
    @abstractmethod
    def execute_search(self, query: str, max_results: int) -> list[dict]:
        raise NotImplementedError