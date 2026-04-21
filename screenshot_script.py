#!/usr/bin/env python3
"""
Screenshot script - takes screenshots of all pages in the auction site.
Usage: python3 screenshot_script.py
"""

import subprocess
import time
import os
import signal
from playwright.sync_api import sync_playwright

# Start the Flask app
print("Starting Flask app...")
proc = subprocess.Popen(
    ["python3", "main.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Wait for server to start
time.sleep(3)

BASE_URL = "http://127.0.0.1:5000"
OUTPUT_DIR = "screenshots"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Pages to screenshot
pages = [
    ("/", "home"),
]


def take_screenshot(page, url, name):
    print(f"Taking screenshot of {url}...")
    full_url = BASE_URL + url if url != "/" else BASE_URL
    try:
        page.goto(full_url, wait_until="networkidle", timeout=10000)
        # Capture only viewport (not full page), same size for all
        page.screenshot(path=f"{OUTPUT_DIR}/{name}.png")
        print(f"Saved: {OUTPUT_DIR}/{name}.png")
    except Exception as e:
        print(f"Error on {url}: {e}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Fixed viewport size for all screenshots
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        for url, name in pages:
            take_screenshot(page, url, name)

        # Now test authenticated pages
        # Login first
        print("Logging in...")
        page.goto(BASE_URL + "/authentication/login")
        page.fill('input[name="user_name"]', "testuser")
        page.fill('input[name="password"]', "password")
        page.click('button[type="submit"]')
        page.wait_for_timeout(1000)

        # Watchlist already has items from database
        print("Watchlist already populated")

        authenticated_pages = [
            ("/listings/mylistings", "my_listings"),
            ("/listings/watchlist", "watchlist"),
            ("/listings/1", "listing_detail"),
        ]

        for url, name in authenticated_pages:
            take_screenshot(page, url, name)

        browser.close()

    print("\nAll screenshots saved!")
    print(f"Output directory: {OUTPUT_DIR}/")


if __name__ == "__main__":
    try:
        main()
    finally:
        # Kill the Flask app
        proc.terminate()
        proc.wait()
