import logging
import os
from dotenv import load_dotenv
from math import log
from utils.pickle_utils import save_as_pickle,load_dict_pickle
from utils.kafka_connect_utils import (get_connectors_status,
                                       restart_connector,
                                       restart_task)
from configs.configs import BackOffConfs

load_dotenv()

log_level = os.getenv("LOG_LEVEL","info").upper()

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

def extract_failed_connectors(connectors_status:dict) -> tuple:
    failed_connectors = tuple(
        map(
            lambda x:x[0],
            filter(
                lambda x:x[1]['connector'] == 'FAILED',
                connectors_status.items()
            )
        )
    )
    return failed_connectors

def extract_failed_tasks(connectors_status:dict) -> list:
    failed_tasks = []
    for conn in connectors_status:
        tasks_stat = connectors_status[conn]['tasks']
        for task_id in tasks_stat:
            if tasks_stat[task_id] == 'FAILED':
                failed_tasks.append((conn,task_id))

    return failed_tasks

def remove_healthy_from_gaurdian_memory_connector(guardian_memory_connector:dict[str,list[int,int]],
                                        failed_connectors:tuple[str]) -> dict:
    for conn in guardian_memory_connector:

        if conn not in failed_connectors:
            guardian_memory_connector.pop(conn)
            logger.debug(f"{conn} removed from "
                         "gaurdian_memory_connector")
    return guardian_memory_connector

def remove_healthy_from_gaurdian_memory_task(guardian_memory_task:dict[str,dict[str,list[int,int]]],
                                        failed_tasks:list[tuple[str,str]]) -> dict:
    for conn in guardian_memory_task:
        task_ids = list(guardian_memory_task[conn].keys())
        for task_id in task_ids:
            if (conn,task_id) not in failed_tasks:
                guardian_memory_task[conn].pop(task_id)
                logger.debug(f"task: {task_id} of {conn} removed from "
                            "gaurdian_memory_task")
    guardian_memory_task = dict(filter(lambda x:x[1] != {},guardian_memory_task.items()))

    return guardian_memory_task


def should_connector_restart(reset:int,
                             seen:int) -> bool:
    if reset == BackOffConfs.max_restart:
        return False
    elif seen == 0 or log(seen,BackOffConfs.exponential_ratio).is_integer():
        return True
    else:
        return False
    
def restart_failed_connectors_and_tasks():
    connectors_status = get_connectors_status()
    if not connectors_status:
        logger.critical("Can't get [b]status[/b] of "
                        "connectors. Please check the logs")
        return None
    
    guardian_memory_connector = load_dict_pickle("guardian_memory_connector.pickle")
    guardian_memory_task = load_dict_pickle("guardian_memory_task.pickle")

    failed_connectors = extract_failed_connectors(connectors_status)
    guardian_memory_connector = remove_healthy_from_gaurdian_memory_connector(
        guardian_memory_connector,
        failed_connectors
    )
    for conn in failed_connectors:
        if conn not in guardian_memory_connector:
            guardian_memory_connector[conn] = [0,0]
        
        reset,seen = guardian_memory_connector[conn]
        
        if not should_connector_restart(reset,seen):
            logger.debug(f"{conn} will be restart later.")
            guardian_memory_connector[conn] = [reset,seen+1]
            continue
        else:
            logger.info(f"Restarting [b]{conn}[/b]..")
            restart_status = restart_connector(conn)
            if restart_status == True:
                logger.info(f"[b]{conn}[/b] "
                            "Restarted [green]successfully[/green]")
            else:
                logger.error(f"Restarting [b]{conn}[/b] "
                            "was [red]failed[/red]")
            guardian_memory_connector[conn] = [reset+1,seen+1]
        save_as_pickle(
            guardian_memory_connector,
            "guardian_memory_connector.pickle")

        failed_tasks = extract_failed_tasks(connectors_status)
        guardian_memory_task = remove_healthy_from_gaurdian_memory_task(
            guardian_memory_task,
            failed_tasks
        )
        for conn,task_id in failed_tasks:
            if conn not in guardian_memory_task:
                guardian_memory_task[conn] = {task_id:[0,0]}
            elif task_id not in guardian_memory_task[conn]:
                guardian_memory_task[conn] = {task_id:[0,0]}
            
            reset,seen = guardian_memory_task[conn][task_id]

            if not should_connector_restart(reset,seen):
                logger.debug(f"taks:{task_id} of {conn} will be restart later.")
                guardian_memory_task[conn][task_id] = [reset,seen+1]
                continue
            else:
                logger.info(f"Restarting task [i]{task_id}[/i] of "
                            f"[b]{conn}[/b]..")
                restart_status = restart_task(conn,task_id)
                if restart_status == True:
                    logger.info(f"task [i]{task_id}[/i] of "
                                f"[b]{conn}[/b] "
                                "Restarted [green]successfully[/green]")
                else:
                    logger.error(f"Restarting task [i]{task_id}[/i] of "
                                f"[b]{conn}[/b] "
                                "was [red]failed[/red]")
                guardian_memory_task[conn][task_id] = [reset+1,seen+1]
        save_as_pickle(
            guardian_memory_task,
            "guardian_memory_task.pickle")

    if not failed_connectors and not failed_tasks:
        logger.info("All tasks and connectors are "
                    "[green]healthy[/green] "
                    "[yellow]:)[/yellow]")