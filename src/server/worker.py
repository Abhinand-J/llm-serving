import threading

from server.engine import InferenceEngine
from server.scheduler import Scheduler


class InferenceWorker:
    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler
        self.engine = InferenceEngine()

        self.thread = threading.Thread(
            target=self.run,
            daemon=True,
        )

    def start(self):
        self.thread.start()

    def run(self):
        while True:
            requests = self.scheduler.get_batch()

            prompts = [request.prompt for request in requests]
            
            print(f"Running batch of {len(requests)} requests")
            results = self.engine.generate_batch(
                prompts,
                max_tokens=requests[0].max_tokens,
            )

            for request, result in zip(requests, results):
                request.future.set_result(result)