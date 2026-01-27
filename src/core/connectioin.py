import threading
from .httprequest import send_request

def request(num, host, port, path, request_delay):
    try:
        # print(f"Thread {num} is starting.")
        result = send_request(host, port, path, request_delay)
        # print(f"Thread {num} finished: {result[:50]}...")  # Print first 50 chars
    except Exception as e:
        print(f"Thread {num} error: {e}")

def numberConnection(num, host, port, path, request_delay):
    threads = []
    for i in range(num):
        thread = threading.Thread(
            target=request,
            args=(i, host, port, path, request_delay),
            daemon=True
        )
        thread.start()
        threads.append(thread)
    
    # print(f"Launched {num} threads")