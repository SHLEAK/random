import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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
urls = {"https://seoulcounseling.com/therapist/dr-jisoo-ahn-psy-d/","https://drjisooahn.wordpress.com/about-dr-jisoo-ahn/","https://www.linkedin.com/in/jisoo-ahn-54278616/"}
been = set()
while urls:
    now = urls.pop()
    print(now)
    been.add(now)
    try:
        new = data(now)
    except:
        new = []
    new = [url for url in new if url not in been and url not in urls]
    urls.update(new)
