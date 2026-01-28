import socket
import time

def send_request(host, port=80, path="/", delay=0, method="GET"):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))

        body = "param1=value1&param2=value2"
        body_bytes = body.encode()
        
        headers = (
            f"{method} {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "User-Agent: MyApp/1.0\r\n"
        )
        
        if method == "POST":
            headers += f"Content-Length: {len(body_bytes)}\r\n"
            headers += "Content-Type: application/x-www-form-urlencoded\r\n"
        
        headers += "Connection: close\r\n"
        headers += "\r\n"  
        
        if method == "GET":
            if delay > 0:
                for b in headers.encode():
                    sock.send(bytes([b]))
                    time.sleep(delay)
            else:
                sock.sendall(headers.encode())
                
        elif method == "POST":
            sock.sendall(headers.encode())
            
            if delay > 0:
                for b in body_bytes:
                    sock.send(bytes([b]))
                    time.sleep(delay)
            else:
                sock.sendall(body_bytes)
        
        response_parts = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_parts.append(chunk)
        
        response = b''.join(response_parts).decode(errors="ignore")
        return True, response
        
    except socket.timeout:
        return False, "Connection timed out"
    except ConnectionRefusedError:
        return False, "Connection refused"
    except socket.gaierror:
        return False, "DNS resolution failed"
    except Exception as e:
        return False, str(e)
    finally:
        if sock:
            sock.close()