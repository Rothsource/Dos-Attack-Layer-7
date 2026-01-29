import socket
import time

def measure_header_read_timeout(host: str, port: int = 80, timeout: float = 10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((host, port))
        sock.send(b"GET / HTTP/1.1\r\n")  # Incomplete HTTP request

        start = time.time()
        try:
            sock.recv(1024)  # Wait for server response or close
            duration = time.time() - start
            sock.close()
            return {"closed_by_server": False, "duration": duration, "error": None}
        except socket.timeout:
            # Server didn’t send data but timeout occurred
            duration = time.time() - start
            sock.close()
            return {"closed_by_server": False, "duration": duration, "error": None}
        except ConnectionResetError:
            # Server closed connection
            duration = time.time() - start
            sock.close()
            return {"closed_by_server": True, "duration": duration, "error": None}

    except Exception as e:
        sock.close()
        return {"closed_by_server": False, "duration": 0, "error": str(e)}

# host = "www.localgrew.com"
# port = 80  # or 443 for HTTPS with TLS (requires SSL wrapper)

# result = measure_header_read_timeout(host, port, timeout=15)

# print(f"Server closed connection: {result['closed_by_server']}")
# print(f"Duration until close/timeout: {result['duration']:.2f} seconds")
# if result["error"]:
#     print(f"Error: {result['error']}")
