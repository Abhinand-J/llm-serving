Serving System for a locally hosted LLM.

Creates a local server to load the LLM. Concurrent requests can be sent to the server and are processed.

Known issues:
1. Assumes all requests in batch have the same max token response length (taken from first request)
2. Assumes a default 10 ms wait time for batching.