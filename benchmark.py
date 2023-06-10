import time
import datetime
def bench():
    start = time.time()
    n = []
    i = 0
    while True:
        n = [n, n]
        i += 1  
        if time.time() - start > 1:
            return i
    return None
while True:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bench_value = bench()
    print(f"Time: {current_time}, Value: {bench_value}")