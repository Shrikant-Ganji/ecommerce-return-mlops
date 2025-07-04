from prefect.client.orchestration import get_client
import asyncio

async def trigger_deployment():
    async with get_client() as client:
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id="ecommerce-return-mlops/Ecommerce Return Pipeline"
        )
        print(f"✅ Deployment triggered! Flow Run ID: {flow_run.id}")

if __name__ == "__main__":
    asyncio.run(trigger_deployment())
