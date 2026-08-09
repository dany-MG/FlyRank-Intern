# FlyRank Week 5 - The polite scrapper

## Target Classification
* **Target Site:** Books to Scrape ([https://books.toscrape.com](https://books.toscrape.com))
* **Purpose:** It is a public practice sandbox built specifically for people to practice scraping on it. This provides explicit permission for this exercise.
* **Scope:** The extraction is strictly limited to the first 3 catalogue pages only.
* **Data Collected:** Book details including title, product URL, price, availability, rating, and description.
* **Robots.txt Result:** no robots file found.
* **Statement:** I will not reuse this code on another site without checking its rules and terms first.

## Setup and Execution (Python Lane)
1. Install dependencies:
```
   pip install requests beautifulsoup4 pydantic
   ```
2. Run the scraper:
```
   python src/main.py
```
## Record Schema
Every valid record adheres to this strict schema:
* title: string
* product_url: string (Absolute URL, acts as canonical identifier)
* price_text: string (Original raw text)
* price_gbp: float (Cleaned numeric value)
* availability_text: string
* rating_text: string (optional/nullable)
* description: string (optional/nullable)
* source_page: string (Provenance)
* fetched_at: string (ISO 8601 timestamp)

## Politeness Rules Followed
* **User-Agent:** Identifies the scraper honestly (FlyRankInternship-A9/1.0).
* **Delay:** Waits at least 0.5 seconds between real network requests.
* **Timeout:** Set to 5.0 seconds to prevent hanging the server or client.
* **Cache:** HTML is saved locally; subsequent runs read from disk to spare the server.

## Honest Limitation
The scraper's extraction logic relies heavily on the specific HTML structure and CSS classes (e.g., `product_pod`, `price_color`). If the site undergoes a frontend redesign, the selectors will break and the scraper will need to be updated.

## Why No Browser?
This assignment needed no browser because all the necessary data is fully present in the raw, static HTML the server sends back upon an HTTP request; spinning up a headless browser would only add unnecessary execution time and memory cost.

## Ethics Note
A professional scraper should always use an official API when one exists. Never bypass logins, paywalls, or server blocks, and always collect only the minimum data you actually need for your task.

## Run Report Evidence
```json
{
  "start_time": "2026-08-09T20:46:55.063306+00:00",
  "end_time": "2026-08-09T20:46:57.121566+00:00",
  "durations_seconds": 2.06,
  "pages_fetched": 0,
  "cache_hits": 60,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}
