from .flipkart import FlipkartScraper
from .amazon import AmazonINScraper

REGISTRY = {
    "Flipkart": FlipkartScraper(),
    "Amazon.in": AmazonINScraper(),
}