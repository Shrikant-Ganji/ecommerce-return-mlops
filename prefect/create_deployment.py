from prefect.client.schemas.schedules import CronSchedule, DeploymentSchedule
from prefect.deployments import Deployment
from prefect.run_monitoring_flow import (
    run_evidently_monitor,
)  # adjust import path if needed

deployment = Deployment.build_from_flow(
    flow=run_evidently_monitor,
    name="scheduled-monitor",
    schedule=DeploymentSchedule(cron=CronSchedule(cron="0 10 * * *"), timezone="UTC"),
    tags=["monitoring"],
    work_queue_name="default",
)

if __name__ == "__main__":
    deployment.apply()
    print("Deployment created and applied successfully.")
