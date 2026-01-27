import socket
import time

def send_request(host, port, path, request_delay=0):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "User-Agent: MyApp/1.0\r\n"
            "Accept: application/json\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        for byte in request.encode():
            sock.send(bytes([byte]))
            time.sleep(request_delay)

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

        sock.close()
        return response.decode(errors="ignore")
    
    except ConnectionResetError:
        return "Connection was reset by server"
    except Exception as e:
        return f"Error: {str(e)}"