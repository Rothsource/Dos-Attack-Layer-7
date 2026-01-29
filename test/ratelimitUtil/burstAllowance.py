import aiohttp
import asyncio
import time
from collections import Counter

URL = "https://www.localgrew.com"

async def send_request(session, url):
    try:
        async with session.get(url) as response:
            return response.status
    except Exception as e:
        return str(e)

async def burst_test(url, num_requests):
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    duration = end_time - start_time

    status_counts = Counter(results)

    # Output summary
    # print("\n=== Burst Rate Limit Test Result ===")
    # print(f"Target URL       : {url}")
    # print(f"Total Requests   : {num_requests}")
    # print(f"Test Duration    : {duration:.2f} seconds")
    # print(f"Requests / Second: {num_requests / duration:.2f}\n")

    # print("Status Code Breakdown:")
    # for status, count in status_counts.items():
    #     print(f"  {status}: {count}")

    # if 429 in status_counts:
    #     print("\n⚠ Rate limiting detected (HTTP 429)")
    # else:
    #     print("\n❌ No rate limiting detected")

    return status_counts

asyncio.run(burst_test(URL, 100))
