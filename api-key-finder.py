import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def search_web_crawler(url):
    pattern = r"sk-[a-z0-9]{40,50}"
    matches = set()

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Accept-Language": "en-US,en;q=0.5",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        base_url = response.url
        urls = [
            urljoin(base_url, link.get("href"))
            for link in soup.find_all("a")
            if link.get("href")
        ]
        matches.update(set(re.findall(pattern, response.text)))
        return urls, matches
    except requests.exceptions.RequestException:
        return [], set()
def main():
    seed_urls = ["https://github.com"]
    visited_urls = set()
    regex_matches = set()

    while seed_urls:
        url = seed_urls.pop(0)

        if url not in visited_urls:
            visited_urls.add(url)
            links, matches = search_web_crawler(url)
            seed_urls += links
            regex_matches.update(matches)

    print("\n".join(regex_matches))
    print("done")
if __name__ == "__main__":
    main()
