from dataclasses import dataclass
from concurrent.futures import Future

@dataclass
class InternalGenerationRequest:
    prompt: str
    max_tokens: int
    future: Future