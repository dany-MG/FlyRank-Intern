import os
import requests

CACHE_DIR = "cache"

os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_page1():
    url = "https://books.toscrape.com/catalogue/page-1.html"
    cache_file = os.path.join(CACHE_DIR, "catalogue-page-1.html")

    if os.path.exists(cache_file):
        with open(cache_file,"r", encoding = "utf-8") as f:
            html_content = f.read()
        print(f"CACHE HIT: {len(html_content)} bytes read from cache")
        return html_content
    else:
        print("CACHE MISS: Fetching page from the web")

    headers = {
        "User-Agent" : "FlyRankInternship-A9/1.0 (+https://github.com/dany-MG/FlyRank-Intern/tree/main/scraper)"
    }

    try:
        res = requests.get(url, headers = headers, timeout = 5)
        if res.status_code == 200:
            html_content = res.text

            with open(cache_file, "w", encoding = "utf-8") as f:
                f.write(html_content)

            print(f"FETCH: {len(html_content)} bytes fetched and cached")
            return html_content
        else:
            print(f"ERROR: Failed to fetch page. Status code: {res.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Resquest failed: {e}")
        return None


if __name__ == "__main__":
    fetch_page1()

        