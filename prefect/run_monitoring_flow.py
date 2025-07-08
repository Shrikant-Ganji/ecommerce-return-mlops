import subprocess

from prefect import flow


@flow(name="Evidently Monitoring Flow")
def run_evidently_monitor():
    subprocess.run(["python", "monitoring/evidently_monitor.py"], check=True)


if __name__ == "__main__":
    run_evidently_monitor()
