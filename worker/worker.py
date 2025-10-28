# worker.py
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
import requests
from datetime import timedelta

# ---- Activity (actual work) ----
@activity.defn(name="fetch_data_from_api")
def fetch_data_from_api():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return response.json()

# ---- Workflow (orchestration logic) ----
@workflow.defn
class ApiWorkflow:
    @workflow.run
    async def run(self):
        result = await workflow.execute_activity(
            "fetch_data_from_api",
            start_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"API result: {result}")
        return result

# ---- Worker setup ----
async def main():
    client = await Client.connect("temporal:7233")  # connect to Temporal inside same Docker network
    worker = Worker(
        client,
        task_queue="api-task-queue",  # your queue name
        workflows=[ApiWorkflow],
        activities=[fetch_data_from_api],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
