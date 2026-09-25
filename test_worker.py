from agents.worker import WorkerAgent

worker = WorkerAgent()

result = worker.execute_task(
    request="Create a business proposal for a coffee shop.",
    task="Write an Executive Summary."
)

print(result)