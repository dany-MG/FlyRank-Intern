import os
import time
import json
import re
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from schema.books_schema import Book
from pydantic import ValidationError

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_html(url, retries = 1):
    filename = url.replace("https://", "").replace("/","_")
    cache_file = os.path.join(CACHE_DIR, filename)

    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding = "utf-8") as f:
            return f.read(), True

    headers = {
        "User-Agent" : "FlyRankInternship-A9/1.0 (+https://github.com/dany-MG/FlyRank-Intern/tree/main/scraper)"
    }

    time.sleep(0.5)

    for attempt in range(retries + 1):
        time.sleep(0.5)
        try:
            res = requests.get(url, headers = headers, timeout = 5)
            if res.status_code == 200:
                with open(cache_file, "w", encoding = "utf-8") as f:
                    f.write(res.text)
                    return res.text, False
            elif res.status_code in (404, 403):
                print(f"Request failed for {url}: {res.status_code} {res.reason}. Skipping...")
                return None, False
            elif res.status_code >= 500:
                print(f"Server error for {url}: {res.status_code} {res.reason}. Retrying...")
                time.sleep(1)
                continue
            else:
                return None, False         
        except requests.RequestException as e:
            print(f"Resquest failed for {url}: {e}. Retrying...")
            time.sleep(1)
            continue
    return None, False

def discover_books():
    current_url = "https://books.toscrape.com/catalogue/page-1.html"
    discovered_links = []
    pages_crawled = 0
    max_pages = 3

    while current_url and pages_crawled < max_pages:
        html, is_cached = fetch_html(current_url)
        if not html:
            break

        status = "CACHE HIT" if is_cached else "FETCHED"
        print(f"{status} : {current_url}")

        soup = BeautifulSoup(html, "html.parser")

        articles = soup.find_all("article", class_ = "product_pod")
        for article in articles:
            relative_url =  article.h3.a["href"]
            absolute_url = urljoin(current_url, relative_url)
            discovered_links.append({"url": absolute_url, "source" : current_url })

        pages_crawled+=1

        next_li = soup.find("li", class_="next")
        if next_li and next_li.a:
            next_relative = next_li.a["href"]
            current_url = urljoin(current_url, next_relative)
        else:
            current_url = None

    unique_books = {}
    for item in discovered_links:
        if item["url"] not in unique_books:
            unique_books[item["url"]] = item["source"]
    return unique_books

def extract_book_details(html, book_url, source_page):
    soup = BeautifulSoup(html, "html.parser")
    product_main = soup.find("div", class_="col-sm-6 product_main")
    title = product_main.h1.text if product_main and product_main.h1 else None
    price_p = product_main.find("p", class_="price_color") if product_main else None
    price_text = price_p.text.strip() if price_p else None

    price_gbp = None
    if price_text:
        match = re.search(r'\d+\.\d+', price_text)
        if match:
            price_gbp = float(match.group())

    availability_p = product_main.find("p", class_="instock availability") if product_main else None
    availability_text = availability_p.text.strip() if availability_p else None

    rating_p = product_main.find("p", class_="star-rating") if product_main else None
    rating_text = rating_p["class"][1] if rating_p and len(rating_p["class"]) > 1 else None

    desc_header = soup.find("div", id="product_description")
    desc_p = desc_header.find_next_sibling("p") if desc_header else None
    description_text = desc_p.text if desc_p else None

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return{
        "title" : title,
        "product_url" : book_url,
        "price_text" : price_text,
        "price_gbp" : price_gbp,
        "availability_text" : availability_text,
        "rating_text" : rating_text,
        "description_text" : description_text,
        "source_page" : source_page,
        "fetched_at" : fetched_at
    }

def validate_record(raw_data):
    os.makedirs("output", exist_ok = True)

    good = []
    bad = []

    for record in raw_data:
        try:
            valid_book = Book(**record)
            good.append(valid_book.model_dump())
        except ValidationError as e:
            bad.append({
                "url" : record.get("product_url" , "unknown"),
                "reason" : json.loads(e.json())
            })

    with open(os.path.join("output", "books.json"), "w", encoding = "utf-8") as f:
        json.dump(good, f, indent = 2, ensure_ascii = False)

    if bad:
        with open("errors.json", "w", encoding = "utf-8") as f:
            json.dump(bad, f, indent = 2, ensure_ascii = False)

    return len(good), len(bad)

if __name__ == "__main__":
    start_time = time.time()
    stats = {
        "pages_fetched": 0,
        "cache_hits": 0,
        "failed_pages": 0,
        "valid_records": 0,
        "invalid_records": 0
    }
    print("-----Crawling Catalogue------")
    unique_books = discover_books()
    unique_books["https://books.toscrape.com/catalogue/fake-book-999/index.html"] = "fake_source"
    print("-----Extracting Book Details------")
    raw_records = []

    for book_url, source_page in unique_books.items():
        try:
            html, is_cached = fetch_html(book_url)
            if html:
                if is_cached:
                    stats["cache_hits"] += 1
                else:
                    stats["pages_fetched"] += 1
                record = extract_book_details(html, book_url, source_page)
                raw_records.append(record)
            else:
                stats["failed_pages"] += 1
        except Exception as e:
            print(f"Unexpected error processing {book_url}: {e}")
            stats["failed_pages"] += 1

    valid_count, invalid_count = validate_record(raw_records)
    stats["valid_records"] = valid_count
    stats["invalid_records"] = invalid_count
    end_time = time.time()

    report = {
        "start_time" : datetime.fromtimestamp(start_time, timezone.utc).isoformat(),
        "end_time" : datetime.fromtimestamp(end_time, timezone.utc).isoformat(),
        "durations_seconds" : round(end_time - start_time, 2),
        "pages_fetched" : stats["pages_fetched"],
        "cache_hits" : stats["cache_hits"],
        "valid_records" : stats["valid_records"],
        "invalid_records" : stats["invalid_records"],
        "failed_pages" : stats["failed_pages"]
    }

    with open(os.path.join("output", "run-report.json"), "w", encoding = "utf-8") as f:
        json.dump(report, f, indent = 2, ensure_ascii = False)

    if raw_records:
        print("\nSample Record:\n")
        print(json.dumps(raw_records[59], indent=2, ensure_ascii=False))

    print(f"\ndetail_pages = {len(raw_records)}")

    print("\n--- Run Report ---")
    print(json.dumps(report, indent=2))
        