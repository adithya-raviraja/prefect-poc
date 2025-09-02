from time import sleep
from prefect import task, get_run_logger

@task
def sleep_for_a_while(seconds: int):
    logger = get_run_logger()
    logger.info(f"Beginning Sleeping for {seconds} seconds...")
    sleep(seconds)
    logger.info(f"Completed Slept for {seconds} seconds")