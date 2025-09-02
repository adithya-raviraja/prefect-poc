from prefect import flow, task, get_run_logger
from poc.sub_function import sleep_for_a_while

@task 
def test_task_function(sleep_duration):
    logger = get_run_logger()
    logger.info("HI FROM THE TASK FUNCTION")
    sleep_for_a_while(sleep_duration)
    from poc.sub_function import sleep_addtional
    sleep_addtional(sleep_duration)
    return

@flow
def test_flow_functions(sleep_duration: int):
    logger = get_run_logger()
    logger.info("HELLO@@@@@ and welcome FROM THE FLOW FUNCTION")
    test_task_function(sleep_duration)
    return