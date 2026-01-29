import requests
import concurrent.futures

TOTAL_REQUESTS = 100
WORKERS = 50


def send_request(URL):
    try:
        r = requests.get(URL, timeout=5)
        return r.status_code
    except requests.RequestException:
        return "ERROR"

def test_rate_limiting(URL):
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        results = list(executor.map(lambda _: send_request(URL), range(TOTAL_REQUESTS)))

    count_200 = results.count(200)
    count_429 = results.count(429)
    count_errors = results.count("ERROR")

    if count_200:
        print(f"Successful responses {count_200}: No Request Rate Limiting Detected")
    elif count_429:
        print(f"Rate limited responses {count_429}: Request Rate Limiting Detected")
    else:
        print(f"Errors encountered {count_errors}: Unable to determine Rate Limiting")
        

URL = "https://www.localgrew.com"
test_rate_limiting(URL)