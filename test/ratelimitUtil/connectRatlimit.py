import socket
import threading

def test_connection_rate_limit(host: str, port: int = 443, total_connections: int = 100, timeout: float = 5):

    results = []

    def connect(idx):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.close()
            results.append((idx, True))
        except:
            results.append((idx, False))

    threads = []
    for i in range(total_connections):
        t = threading.Thread(target=connect, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success = sum(1 for _, r in results if r)
    fail = sum(1 for _, r in results if not r)

    return {
        "total": total_connections,
        "success": success,
        "fail": fail,
        "results": results
    }


# # host = "www.localgrew.com"
# # result = test_connection_rate_limit(host, port=443, total_connections=100)

# # print(f"Total attempted connections: {result['total']}")
# # print(f"Successful connections: {result['success']}")
# # print(f"Failed connections: {result['fail']}")

# if result["fail"] > 0:
#     print("Some connections were blocked — possible connection rate limiting")
# else:
#     print("All connections succeeded — no connection-level rate limiting detected")
