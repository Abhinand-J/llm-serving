import time

from server.engine import InferenceEngine


def main():
    engine = InferenceEngine()

    prompt = "Explain virtual memory in one paragraph."
    max_tokens = 100

    inputs = engine.tokenizer(prompt, return_tensors="pt")
    input_tokens = inputs["input_ids"].shape[1]

    start = time.perf_counter()

    result = engine.generate(prompt, max_tokens)

    elapsed = time.perf_counter() - start

    output_tokens = len(
        engine.tokenizer.encode(result, add_special_tokens=False)
    )

    print(f"Time taken: {elapsed:.3f} seconds")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Tokens/sec: {output_tokens / elapsed:.2f}")
    print(f"\nGenerated text:\n{result}")


if __name__ == "__main__":
    main()