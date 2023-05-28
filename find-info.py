from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import webbrowser
def data(url):
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            if href.startswith('http'): 
                absolute_url = href
            else:
                absolute_url = urljoin(url, href) 
            links.append(absolute_url)
    return links
urls = {"https://stackoverflow.com"}
been = set()
while urls:
    now = urls.pop()
    print(now)
    webbrowser.open(now)
    been.add(now)
    try:
        new = data(now)
    except Exception as e:
        new = []
    except KeyboardInterrupt:
        break
    new = [url for url in new if url not in been and url not in urls]
    urls.update(new)
