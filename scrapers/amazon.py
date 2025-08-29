from typing import Iterable, Dict
import requests, re
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9"
}

class AmazonINScraper:
    base = "https://www.amazon.in/s"

    def search(self, query: str, page: int) -> Iterable[Dict]:
        params = {"k": query, "page": str(page)}
        resp = requests.get(self.base, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for c in soup.select("div.s-result-item"):
            name_tag = c.select_one("h2 a span")
            if not name_tag:
                continue
            name = name_tag.get_text(strip=True)
            link = c.select_one("h2 a")
            url = "https://www.amazon.in" + link.get("href") if link and link.get("href","").startswith("/") else (link.get("href") if link else "")

            price_whole = c.select_one("span.a-price > span.a-offscreen")
            price = price_whole.get_text(strip=True) if price_whole else ""
            rating_tag = c.select_one("span.a-icon-alt")
            rating = rating_tag.get_text(strip=True) if rating_tag else ""

            if name and price:
                yield {"name": name, "price": price, "rating": rating or "N/A", "url": url}