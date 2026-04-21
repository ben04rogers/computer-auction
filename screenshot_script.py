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

# Pages to screenshot (unauthenticated)
pages = [
    ("/", "home"),
]


def take_screenshot(page, url, name):
    print(f"Taking screenshot of {url}...")
    full_url = BASE_URL + url if url != "/" else BASE_URL
    try:
        page.goto(full_url, wait_until="networkidle", timeout=10000)
        page.screenshot(path=f"{OUTPUT_DIR}/{name}.png")
        print(f"Saved: {OUTPUT_DIR}/{name}.png")
    except Exception as e:
        print(f"Error on {url}: {e}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        for url, name in pages:
            take_screenshot(page, url, name)

        # Login first
        print("Logging in...")
        page.goto(BASE_URL + "/authentication/login")
        page.fill('input[name="user_name"]', "testuser")
        page.fill('input[name="password"]', "password")
        page.click('button[type="submit"]')
        page.wait_for_timeout(1000)

        # Authenticated pages
        authenticated_pages = [
            ("/listings/create", "create_listing"),
            ("/listings/mylistings", "my_listings"),
            ("/listings/watchlist", "watchlist"),
            ("/listings/2", "listing_detail"),
        ]

        for url, name in authenticated_pages:
            take_screenshot(page, url, name)

        # Screenshot with reviews section visible - scroll down to it
        print("Taking screenshot of reviews section...")
        page.goto(BASE_URL + "/listings/2?tab=reviews", wait_until="networkidle")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.7)")
        page.wait_for_timeout(500)
        page.screenshot(path=f"{OUTPUT_DIR}/listing_reviews.png")
        print(f"Saved: {OUTPUT_DIR}/listing_reviews.png")

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
