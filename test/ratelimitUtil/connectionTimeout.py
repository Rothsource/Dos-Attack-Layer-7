import socket
import time

def measure_connection_timeout(host: str, port: int = 443, timeout: float = 1):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    start = time.time()

    try:
        sock.connect((host, port))
        try:
            # Try receiving 1 byte (will block until timeout)
            sock.recv(1)
            duration = time.time() - start
            sock.close()
            return {"success": True, "timeout": False, "duration": duration, "error": None}
        except socket.timeout:
            duration = time.time() - start
            sock.close()
            return {"success": True, "timeout": True, "duration": duration, "error": None}
    except Exception as e:
        duration = time.time() - start
        sock.close()
        return {"success": False, "timeout": False, "duration": duration, "error": str(e)}
    
host = "www.localgrew.com"
port = 443

result = measure_connection_timeout(host, port, timeout=2)

print(f"Success: {result['success']}")
print(f"Timeout: {result['timeout']}")
print(f"Duration: {result['duration']:.2f} seconds")
if result["error"]:
    print(f"Error: {result['error']}")

