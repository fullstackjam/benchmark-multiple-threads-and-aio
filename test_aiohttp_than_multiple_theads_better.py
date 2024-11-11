import time
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor

# Example API URL
URL = "http://localhost:8000/slow"

# Number of requests
NUM_REQUESTS = 200
# Thread pool size
POOL_SIZE = 10  # Adjust as needed

# Blocking requests in a loop
def fetch_request_in_loop():
    response = []
    for _ in range(NUM_REQUESTS):
        response.append(requests.get(URL))
    return response

# Asynchronous requests using aiohttp
async def fetch_aiohttp(session, url):
    async with session.get(url) as response:
        return await response.json()

async def run_aiohttp():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_aiohttp(session, URL) for _ in range(NUM_REQUESTS)]
        return await asyncio.gather(*tasks)

# Multithreaded requests
def fetch_requests(url):
    response = requests.get(url)
    return response.json()

def run_multithreading():
    with ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
        futures = [executor.submit(fetch_requests, URL) for _ in range(NUM_REQUESTS)]
        results = [future.result() for future in futures]
    return results

# Testing function
def test_comparison():
    # Test loop blocking requests
    start_time = time.time()
    fetch_request_in_loop()
    loop_http_duration = time.time() - start_time
    print(f"Loop HTTP duration: {loop_http_duration:.2f} seconds")

    # Test aiohttp performance
    start_time = time.time()
    asyncio.run(run_aiohttp())
    aiohttp_duration = time.time() - start_time
    print(f"aiohttp duration: {aiohttp_duration:.2f} seconds")

    # Test multithreading performance
    start_time = time.time()
    run_multithreading()
    threading_duration = time.time() - start_time
    print(f"Multithreading duration: {threading_duration:.2f} seconds")

    # Result comparison
    print(f"aiohttp is faster than multithreading by {(threading_duration - aiohttp_duration) / threading_duration * 100:.2f}%")

# Execute tests
if __name__ == "__main__":
    test_comparison()
