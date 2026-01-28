import threading
from .httprequest import send_request

def request(host, port, path, request_delay, method):
    try:
        result = send_request(host, port, path, request_delay, method)
        # print(f"Request completed: {result[0]}")
    except Exception as e:
        print(f"Thread error: {e}")

def numberConnection(num, host, port, path, request_delay, method):
    threads = []
    for i in range(num):
        thread = threading.Thread(
            target=request,
            args=(host, port, path, request_delay, method),
            daemon=True
        )
        thread.start()
        threads.append(thread)
    
    # for thread in threads:
    #     thread.join()
    
    # print(f"All {num} threads completed")