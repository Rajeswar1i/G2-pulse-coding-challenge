#!/usr/bin/env python3
"""
scraper_review.py

Fetch G2 reviews using the JSON API with authentication to bypass 403 errors.
"""

import json
import time
import pickle
from datetime import datetime
from typing import List, Dict

import requests
from dateutil.parser import parse as parse_date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

COOKIE_FILE = "g2_cookies.pkl"  # Selenium login cookies

def in_range(d: datetime, start: datetime, end: datetime) -> bool:
    return start <= d <= end

def write_json(out_path: str, reviews: List[Dict]):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

# ----------------- G2 Scraper -----------------
class G2Scraper:
    def __init__(self, company_url: str, start: datetime, end: datetime, cookies: list, max_retries: int = 3):
        self.company_url = company_url.rstrip("/") + "/reviews.json"
        self.start = start
        self.end = end
        self.cookies = cookies
        self.max_retries = max_retries

    def fetch_page(self, page: int):
        url = f"{self.company_url}?page={page}"
        retries = 0
        while retries < self.max_retries:
            try:
                r = requests.get(url, headers=HEADERS, cookies={c['name']: c['value'] for c in self.cookies}, timeout=15)
                if r.status_code != 200:
                    raise Exception(f"Status code {r.status_code}")
                data = r.json()
                if "reviews" not in data or len(data["reviews"]) == 0:
                    print(f"No reviews on page {page}")
                    return []
                return data["reviews"]
            except Exception as e:
                retries += 1
                print(f"Failed to fetch page {page} (retry {retries}/{self.max_retries}): {e}")
                time.sleep(2)
        return []

    def scrape(self) -> List[Dict]:
        reviews = []
        page = 1
        while True:
            page_reviews = self.fetch_page(page)
            if not page_reviews:
                break
            for r in page_reviews:
                parsed_date = parse_date(r.get("date") or r.get("created_at"))
                if not in_range(parsed_date, self.start, self.end):
                    continue
                reviews.append({
                    "title": r.get("title"),
                    "description": r.get("text") or r.get("body"),
                    "date": parsed_date.isoformat(),
                    "reviewer": r.get("user_name") or r.get("author"),
                    "rating": float(r.get("rating") or 0),
                    "source": "g2",
                    "url": r.get("url")
                })
            page += 1
            time.sleep(1)  # polite delay
        return reviews

# ----------------- Main -----------------
if __name__ == "__main__":
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    url = "https://www.g2.com/products/slack"

    # Load cookies for authenticated requests
    try:
        cookies = pickle.load(open(COOKIE_FILE, "rb"))
    except FileNotFoundError:
        # If no cookies, launch Selenium for manual login
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get("https://www.g2.com/login")
        input("Log in manually, then press Enter here...")
        cookies = driver.get_cookies()
        pickle.dump(cookies, open(COOKIE_FILE, "wb"))
        driver.quit()
        print("Cookies saved. You can now run the scraper headless.")

    scraper = G2Scraper(url, start, end, cookies)
    reviews = scraper.scrape()

    print(f"Collected {len(reviews)} reviews")
    write_json("slack_reviews.json", reviews)
