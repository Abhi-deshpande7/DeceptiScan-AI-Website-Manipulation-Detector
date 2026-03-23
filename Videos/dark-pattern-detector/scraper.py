import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import base64
import os

def scrape_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        buttons    = [b.get_text(strip=True) for b in soup.find_all("button")]
        links      = [a.get_text(strip=True) for a in soup.find_all("a") if a.get_text(strip=True)]
        checkboxes = [c.get("name", "") for c in soup.find_all("input", {"type": "checkbox"})]
        headings   = [h.get_text(strip=True) for h in soup.find_all(["h1","h2","h3"])]
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        page_title = soup.title.string if soup.title else "No title"

        return {
            "url": url,
            "title": page_title,
            "buttons": buttons[:30],
            "links": links[:40],
            "checkboxes": checkboxes[:20],
            "headings": headings[:20],
            "paragraphs": paragraphs[:30]
        }
    except Exception as e:
        return {"error": str(e)}

def take_screenshot(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(url, timeout=15000)
            page.wait_for_timeout(2000)
            screenshot_bytes = page.screenshot(full_page=False)
            browser.close()
            encoded = base64.b64encode(screenshot_bytes).decode("utf-8")
            return encoded
    except Exception as e:
        return None