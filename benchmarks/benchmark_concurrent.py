import time
from concurrent.futures import ThreadPoolExecutor

import requests

URL = "http://127.0.0.1:8000/generate"

PROMPTS = [
    "Explain virtual memory.",
    "What is a process and how is it different from a thread?",
    "What does a thread-local variable mean in C++?",
    "Explain what an algorithm is.",
    "What is a mutex and why is it useful?",
    "Explain what a cache is in computer architecture.",
    "What is the difference between TCP and UDP?",
    "Explain how a hash table works.",
]


def send_request(prompt):
    start = time.perf_counter()

    response = requests.post(
        URL,
        json={
            "prompt": prompt,
            "max_tokens": 100,
        },
    )

    elapsed = time.perf_counter() - start

    response.raise_for_status()

    return elapsed, response.json()["text"]


def benchmark(num_requests):
    prompts = PROMPTS[:num_requests]
    if num_requests > 8:
        prompts = prompts * int(num_requests / 8)

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        results = list(executor.map(send_request, prompts))

    total_time = time.perf_counter() - start

    total_tokens = num_requests * 100
    throughput = total_tokens / total_time

    print(f"\n=== {num_requests} concurrent requests ===")

    for i, (latency, text) in enumerate(results):
        print(f"Request {i}: {latency:.3f}s")

    print(f"Total time: {total_time:.3f}s")
    print(f"Aggregate tokens/sec: {throughput:.2f}")


for num_requests in [1, 4, 16, 64]:
    benchmark(num_requests)