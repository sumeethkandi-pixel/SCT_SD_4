from abc import ABC, abstractmethod
from typing import Iterable, Dict

class BaseScraper(ABC):
    @abstractmethod
    def search(self, query: str, page: int) -> Iterable[Dict]:
        """Yield dicts with keys: name, price, rating, url"""
        ...

    @property
    def display_name(self) -> str:
        return self.__class__.__name__