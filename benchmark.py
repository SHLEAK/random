import time
import datetime
def bench():
    start_time = time.time()
    iterations = 0
    while time.time() - start_time < 1:
        iterations += 1
    return iterations
while True:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bench_value = bench()
    print(f"Time: {current_time}, Value: {bench_value}")
