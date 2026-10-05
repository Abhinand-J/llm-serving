from server.engine import InferenceEngine

def main():
    engine = InferenceEngine()

    result = engine.generate(
        "Explain what virtual memory is in one paragraph.",
        max_tokens=100
    )

    print(result)


if __name__ == "__main__":
    main()