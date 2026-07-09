from airflow.sdk import dag,task
from airflow.operators.bash import BashOperator
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunLifeCycleState, RunResultState
import time

@dag
def orchestra():

    @task
    def ingest_cdc():
        ws = WorkspaceClient(
        host="https://dbc-e417c4cb-347a.cloud.databricks.com",
        token=""
        )

        job_trigger = ws.jobs.run_now(job_id=218599483792827)

        while True:

            job_run = ws.jobs.get_run(job_trigger.run_id)

            if job_run.state.life_cycle_state in [RunLifeCycleState.TERMINATED, RunLifeCycleState.SKIPPED, RunLifeCycleState.INTERNAL_ERROR]:
                if job_run.state.result_state == RunResultState.SUCCESS:
                    print("Job completed successfully!")
                    break 
                else:
                    raise Exception(f"Job failed with state: {job_run.state.result_state}")
                    
            time.sleep(5)  # Wait for 5 seconds before checking the job status again
        
        return "CDC Ingestion Completed"
    

    @task
    def clean_target():
        return "rm -rf /opt/airflow/walmart_project/target && rm -rf /opt/airflow/walmart_project/logs"
    
    @task.bash
    def source_freshness():
        # Manually set the working directory using the 'cd' command before executing the dbt command
        return "cd /opt/airflow/walmart_project && dbt source freshness"
    

    silver_technical = BashOperator(
        task_id='silver_technical',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select silver_technical'
    )

    silver_technical_tests = BashOperator(
        task_id='silver_technical_tests',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt test --select silver_technical'
    )
    silver_business = BashOperator(
        task_id='silver_business',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select silver_business'
    )

    silver_business_tests = BashOperator(
        task_id='silver_business_tests',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt test --select silver_business'
    )

    gold_ephermeral = BashOperator(
        task_id='gold_ephermeral',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select gold/ephermeral'
    )

    gold_dimensions = BashOperator(
        task_id='gold_dimensions',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt snapshot'
    )

    gold_facts = BashOperator(
        task_id='gold_facts',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select gold/fact'
    )


    
    ingest_cdc() >> clean_target() >> source_freshness() >> silver_technical >> silver_technical_tests >> silver_business >> silver_business_tests >> gold_ephermeral >> gold_dimensions >> gold_facts

orestra_dag = orchestra()
