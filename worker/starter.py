# starter.py
import asyncio
from temporalio.client import Client

async def main():
    client = await Client.connect("temporal:7233")
    handle = await client.start_workflow(
        "ApiWorkflow",
        id="api-workflow-001",
        task_queue="api-task-queue",
    )
    print(f"Started workflow: {handle.id}")

if __name__ == "__main__":
    asyncio.run(main())
