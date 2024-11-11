import time
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor

# Example API URL
URL = "http://localhost:8000/fast"

# Number of requests
NUM_REQUESTS = 5
# Thread pool size
POOL_SIZE = 5  # Adjust as needed

# Data processing function (simulating CPU-intensive task)
def process_data(data):
    # Simulate some computational operations
    result = 0
    for i in range(10000000):
        result += i * data.get("id", 1)
    return result

# Asynchronous requests using aiohttp
async def fetch_aiohttp(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return process_data(data)  # Adding CPU-intensive task

async def run_aiohttp():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_aiohttp(session, URL) for _ in range(NUM_REQUESTS)]
        return await asyncio.gather(*tasks)

# Multithreaded requests
def fetch_requests(url):
    response = requests.get(url)
    data = response.json()
    return process_data(data)  # Adding CPU-intensive task

def run_multithreading():
    with ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
        results = list(executor.map(fetch_requests, [URL] * NUM_REQUESTS))
    return results

# Test function
def test_comparison():
    # Testing aiohttp performance
    start_time = time.time()
    asyncio.run(run_aiohttp())
    aiohttp_duration = time.time() - start_time
    print(f"aiohttp duration: {aiohttp_duration:.2f} seconds")

    # Testing multithreading performance
    start_time = time.time()
    run_multithreading()
    threading_duration = time.time() - start_time
    print(f"Multithreading duration: {threading_duration:.2f} seconds")

    # Results comparison
    print(f"Multithreading is faster than aiohttp by {(aiohttp_duration - threading_duration) / aiohttp_duration * 100:.2f}%")

# Run test
if __name__ == "__main__":
    test_comparison()
