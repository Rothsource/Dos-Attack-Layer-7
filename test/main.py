import requests
from scanServer import scan_server



def scan_url(url):
    print("\n\nServer Identification...")
    print("="*40)
    scan_server(url)
    
    print("\n\nRate Limiting...")
    print("="*40)

    response = requests.get(url)

    # # Check rate limit headers
    # rate_limit = response.headers.get('X-RateLimit-Limit')
    # retry_after = response.headers.get('Retry-After')
    # rate_limit_reset = response.headers.get('X-RateLimit-Reset')
    # rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
    
    # print("Rate Limiting Headers: {rate_limit}")
    # print(f"Retry-After: {retry_after}")
    # print(f"X-RateLimit-Reset: {rate_limit_reset}")
    # print(f"X-RateLimit-Remaining: {rate_limit_remaining}")

url = input("Enter URL to scan: ")
scan_url(url)