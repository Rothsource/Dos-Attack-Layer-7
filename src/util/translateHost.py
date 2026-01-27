from urllib.parse import urlparse

"""Parse URL and return host, port, and path"""

def parse_url(url):

    parsed = urlparse(url)
    
    host = parsed.hostname
    
    if parsed.port:
        port = parsed.port
    else:
        port = 443 if parsed.scheme == 'https' else 80
    
    path = parsed.path if parsed.path else '/'
    
    return host, port, path

