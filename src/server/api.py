from concurrent.futures import Future

from fastapi import FastAPI
from pydantic import BaseModel

from server.request import InternalGenerationRequest
from server.request_manager import RequestManager
from server.scheduler import Scheduler
from server.worker import InferenceWorker


app = FastAPI()

request_manager = RequestManager()
scheduler = Scheduler(request_manager, batch_size=128)
worker = InferenceWorker(scheduler)
worker.start()


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100


@app.post("/generate")
def generate(request: GenerateRequest):
    future = Future()

    generation_request = InternalGenerationRequest(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        future=future,
    )

    request_manager.submit(generation_request)

    result = future.result()

    return {"text": result}