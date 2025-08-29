# E‑commerce Product Scraper (GUI)

A real‑time desktop GUI that scrapes product **name, price, rating** from Amazon.in or Flipkart
and lets you **export to CSV**. Built with Tkinter + BeautifulSoup.

> ⚠️ Use responsibly. Follow each website’s Terms of Service and robots.txt. This project is for learning.

## Features
- Provider selector: **Amazon** or **Flipkart**
- Live results table
- Page count (1–5) to fetch multiple pages
- Export to CSV (UTF‑8)
- Robust parsing with fallbacks and user‑agent headers

## Quick Start
1. Create & activate a virtualenv (optional but recommended)
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app
   ```bash
   python main.py
   ```

## How to use
1. Pick a **Provider** (Amazon or Flipkart).
2. Enter a **Search Query** (e.g., `laptop`).
3. Choose how many **Pages** to fetch (start with 1–3).
4. Click **Scrape** to see live results.
5. Click **Export CSV** to save `products.csv` in the app folder.

## Notes
- Amazon/Flipkart frequently change HTML; selectors here are best‑effort and may need tweaks.
- If a site blocks requests, try fewer pages, different keywords, or slower speeds.
- You can extend by adding a new scraper file under `scrapers/` and registering it in `scrapers/__init__.py`.