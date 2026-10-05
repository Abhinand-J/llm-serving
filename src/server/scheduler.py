import queue
import time

from server.request import InternalGenerationRequest
from server.request_manager import RequestManager


class Scheduler:
    def __init__(
        self,
        request_manager: RequestManager,
        batch_size: int = 4,
        batch_timeout: float = 0.01,
    ):
        self.request_manager = request_manager
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout

    def get_batch(self) -> list[InternalGenerationRequest]:
        # Always wait for the first request.
        first = self.request_manager.get_next()
        batch = [first]

        # Give other requests a short opportunity to arrive.
        deadline = time.monotonic() + self.batch_timeout

        while len(batch) < self.batch_size:
            remaining = deadline - time.monotonic()

            if remaining <= 0:
                break

            try:
                request = self.request_manager.get_next(timeout=remaining)
                batch.append(request)
            except queue.Empty:
                time.sleep(min(0.001, remaining))

        return batch