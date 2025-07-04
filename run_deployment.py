from prefect.client.orchestration import get_client
from prefect.deployments import run_deployment
import asyncio

async def trigger_deployment():
    async with get_client() as client:
        deployment_id = await run_deployment(
            name="ecommerce-return-mlops/mlops-pipeline",
            client=client,
            parameters={}
        )
        print(f"✅ Deployment triggered! Run ID: {deployment_id}")

if __name__ == "__main__":
    asyncio.run(trigger_deployment())
