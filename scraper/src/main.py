import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_html(url):
    filename = url.split("/")[-1]
    if not filename.endswith(".html"):
        filename ="index.html"
    cache_file = os.path.join(CACHE_DIR, filename)

    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding = "utf-8") as f:
            return f.read(), True

    headers = {
        "User-Agent" : "FlyRankInternship-A9/1.0 (+https://github.com/dany-MG/FlyRank-Intern/tree/main/scraper)"
    }

    time.sleep(0.5)

    try:
        res = requests.get(url, headers = headers, timeout = 5)
        if res.status_code == 200:
            html_content = res.text
            with open(cache_file, "w", encoding = "utf-8") as f:
                f.write(html_content)
            print(f"FETCH: {len(html_content)} bytes fetched and cached")
            return html_content, False
        else:
            print(f"ERROR: Failed to fetch {url} Status code: {res.status_code}")
            return None, False
    except requests.RequestException as e:
        print(f"Resquest failed for {url}: {e}")
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
            discovered_links.append(absolute_url)

        pages_crawled+=1

        next_li = soup.find("li", class_="next")
        if next_li and next_li.a:
            next_relative = next_li.a["href"]
            current_url = urljoin(current_url, next_relative)
        else:
            current_url = None

    unique_links = list(set(discovered_links))

    print(f"catalogue_pages = {pages_crawled}, discovered_books = {len(discovered_links)}, unique_urls = {len(unique_links)}")
    return unique_links

if __name__ == "__main__":
    discover_books()

        