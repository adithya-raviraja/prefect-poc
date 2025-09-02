from time import sleep
from prefect import task, get_run_logger

@task
def sleep_for_a_while(seconds: int):
    print(f"Sleeping for {seconds} seconds...")
    sleep(seconds)
    print(f"Slept for {seconds} seconds")