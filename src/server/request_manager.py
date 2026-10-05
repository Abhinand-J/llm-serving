from queue import Queue

from server.request import InternalGenerationRequest


class RequestManager:
    def __init__(self):
        self.queue = Queue()

    # submit a request to the queue
    def submit(self, request: InternalGenerationRequest):
        self.queue.put(request)

    # get next prompt/request job
    def get_next(self, timeout=None) -> InternalGenerationRequest:
        return self.queue.get(timeout=timeout)