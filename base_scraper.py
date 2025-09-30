import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class BaseScraper:
    def __init__(self, company_name, start, end, use_selenium=False, driver=None):
        self.company_name = company_name
        self.start = start
        self.end = end
        self.use_selenium = use_selenium
        self.driver = driver

        if self.use_selenium and self.driver is None:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            self.driver = webdriver.Chrome(options=options)

    def fetch(self, url: str) -> str:
        """Fetch page HTML using Selenium or Requests"""
        if self.use_selenium:
            try:
                self.driver.get(url)
                time.sleep(2)  # allow page to load
                return self.driver.page_source
            except Exception as e:
                raise Exception(f"Selenium fetch failed for {url}: {e}")
        else:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            return resp.text

    def close(self):
        """Close Selenium driver if used"""
        if self.driver:
            self.driver.quit()
