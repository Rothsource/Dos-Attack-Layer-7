import ssl
import socket
import time

def tls_handshake_test(host, port=443, timeout=5):

    result = {
        "host": host,
        "port": port,
        "handshake_time": None,
        "success": False,
        "error": None,
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    context = ssl.create_default_context()

    try:
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        start = time.time()
        ssl_sock.connect((host, port))
        end = time.time()
        result["handshake_time"] = end - start
        result["success"] = True
        ssl_sock.close()
    except Exception as e:
        result["error"] = str(e)
        sock.close()

    return result

host = "www.localgrew.com"

result = tls_handshake_test(host)
print("TLS Handshake Test Result:")
for k, v in result.items():
    print(f"{k}: {v}")
