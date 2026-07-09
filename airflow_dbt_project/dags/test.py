from databricks.sdk import WorkspaceClient
import time
ws = WorkspaceClient(
    host = "https://dbc-e417c4cb-347a.cloud.databricks.com",
    token= ""
)

job_trigger=ws.jobs.run_now(job_id = 218599483792827) 

while True:
    job_status=ws.jobs.get_run(run_id=job_trigger.run_id)
    if job_status.state.life_cycle_state in ["TERMINATED", "SKIPPED", "INTERNAL_ERROR"]:
        print(f"Job finished with state: {job_status.state.result_state}")
        break
    else:
        print(f"Job is still running. Current state: {job_status.state.life_cycle_state}")
time.sleep(5)  # Wait for 5 seconds before checking the status again