import logging
import os
from dotenv import load_dotenv
from rich.logging import RichHandler 
from utils.kafka_connect_utils import (get_connectors_status,
                                       restart_connector,
                                       restart_task)

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

def restart_failed_connectors_and_tasks():
    connectors_status = get_connectors_status()
    if not connectors_status:
        logger.critical("Can't get [b]status[/b] of "
                        "connectors. Please check the logs")
        return None
    
    failed_connectors = extract_failed_connectors(connectors_status)
    for conn in failed_connectors:
        logger.info(f"Restarting [b]{conn}[/b]..")
        restart_status = restart_connector(conn)
        if restart_status == True:
            logger.info(f"[b]{conn}[/b] "
                        "Restarted [green]successfully[/green]")
        else:
            logger.error(f"Restarting [b]{conn}[/b] "
                        "was [red]failed[/red]")
            
    failed_tasks = extract_failed_tasks(connectors_status)
    for conn,task_id in failed_tasks:
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
    if not failed_connectors and not failed_tasks:
        logger.info("All tasks and connectors are "
                    "[green]healthy[/green] "
                    "[yellow]:)[/yellow]")