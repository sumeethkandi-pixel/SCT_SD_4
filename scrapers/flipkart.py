from typing import Iterable, Dict
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

class FlipkartScraper:
    base = "https://www.flipkart.com/search"

    def search(self, query: str, page: int) -> Iterable[Dict]:
        params = {"q": query, "page": str(page)}
        resp = requests.get(self.base, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Product cards can vary; handle common layouts
        cards = soup.select("div._1AtVbE")
        for c in cards:
            # Name
            name_tag = c.select_one("a.IRpwTa") or c.select_one("a.s1Q9rs") or c.select_one("div._4rR01T")
            if not name_tag:
                continue
            name = (name_tag.get_text(strip=True) if name_tag.name != "div" else name_tag.get_text(strip=True))

            # URL
            href = name_tag.get("href") or ""
            url = ("https://www.flipkart.com" + href) if href.startswith("/") else href

            # Price
            price_tag = c.select_one("div._30jeq3") or c.select_one("div._3I9_wc")
            price = price_tag.get_text(strip=True) if price_tag else ""

            # Rating
            rating_tag = c.select_one("div._3LWZlK") or c.select_one("span._2_R_DZ")
            rating = rating_tag.get_text(strip=True) if rating_tag else ""

            if name and price:
                yield {"name": name, "price": price, "rating": rating or "N/A", "url": url}