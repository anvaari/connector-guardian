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

class ConnectorRestarter():
    
    def __init__(self) -> None:
        self.guardian_memory_connector:dict[str,list[int]] = load_dict_pickle("guardian_memory_connector.pickle")
        self.guardian_memory_task:dict[str,dict[int,list[int]]] = load_dict_pickle("guardian_memory_task.pickle")

    def extract_failed_connectors(self, connectors_status: dict) -> list[str]:
        return [connector for connector, status in connectors_status.items() if status['connector'] == 'FAILED']

    def extract_failed_tasks(self, connectors_status: dict) -> list[tuple[str,int]]:
        failed_tasks = []
        for conn in connectors_status:
            tasks_stat = connectors_status[conn]['tasks']
            for task_id in tasks_stat:
                if tasks_stat[task_id] == 'FAILED':
                    failed_tasks.append((conn,task_id))
        return failed_tasks
    
    def remove_healthy_from_guardian_memory_connector(self, failed_connectors: list[str]) -> None:
        self.guardian_memory_connector:dict[str,list[int]] = {conn: status
                                                          for conn, status in self.guardian_memory_connector.items()
                                                          if conn in failed_connectors}

    def remove_healthy_from_guardian_memory_task(self, failed_tasks: list[tuple[str,int]]):
        for conn in list(self.guardian_memory_task.keys()):
            for task_id in list(self.guardian_memory_task[conn].keys()):
                if (conn,task_id) not in failed_tasks:
                    self.guardian_memory_task[conn].pop(task_id)
                    
        self.guardian_memory_task = dict(
            filter(lambda x:x[1] != {},self.guardian_memory_task.items())
        )

    def should_connector_restart(self,
                                 reset:int,
                                 seen:int) -> bool:
        if not BackOffConfs.is_enabled :
            return True
        if reset == BackOffConfs.max_restart:
            logger.debug("Connector reach the maximum restart limit")
            return False
        if seen == 0:
            return True
        elif BackOffConfs.exponential_ratio == 1:
            return True
        elif log(seen,BackOffConfs.exponential_ratio).is_integer():
            return True
        else:
            return False
    
    def restart_connector(self, connector:str) -> None:
        reset, seen = self.guardian_memory_connector.get(connector, [0, 0])

        if not self.should_connector_restart(reset, seen):
            logger.debug(f"{connector} will be restarted later.")
            self.guardian_memory_connector[connector] = [reset, seen + 1]
            return

        restart_status = restart_connector(connector)
        if restart_status:
            logger.info(f"[b]{connector}[/b] "
                        "Restarted {reset} out of "
                        f"{BackOffConfs.max_restart} times "
                        "[green]successfully[/green]")
        else:
            logger.error(f"Restarting [b]{connector}[/b] "
                         "was [red]failed[/red]")

        self.guardian_memory_connector[connector] = [reset + 1, seen + 1]

    def restart_task(self, connector:str, task_id:int) -> None:
        reset, seen = self.guardian_memory_task.get(connector,{}).get(task_id,[0,0])

        if not self.should_connector_restart(reset, seen):
            logger.debug(f"Task {task_id} of [b]{connector}[/b] "
                         "will be restarted later.")
            self.guardian_memory_task.update(
                {connector:{task_id:[reset, seen + 1]}}
            )
            return

        restart_status = restart_task(connector, task_id)
        if restart_status:
            logger.info(f"task [i]{task_id}[/i] of "
                        f"[b]{connector}[/b] "
                        f"Restarted {reset} out of "
                        f"{BackOffConfs.max_restart} times "
                        "[green]successfully[/green]")
        else:
            logger.error(f"Restarting task [i]{task_id}[/i] of "
                         f"[b]{connector}[/b] "
                         "was [red]failed[/red]")
        self.guardian_memory_task.update(
            {connector:{task_id:[reset + 1, seen + 1]}}
        )

    def restart_failed_connectors_and_tasks(self) -> None:
        connectors_status = get_connectors_status()
        if not connectors_status:
            logger.critical("Can't get [b]status[/b] of "
                            "connectors. Please check the logs")
            return

        failed_connectors = self.extract_failed_connectors(connectors_status)
        self.remove_healthy_from_guardian_memory_connector(failed_connectors)

        for conn in failed_connectors:
            self.restart_connector(conn)

        failed_tasks = self.extract_failed_tasks(connectors_status)
        self.remove_healthy_from_guardian_memory_task(failed_tasks)

        for conn,task_id in failed_tasks:
            self.restart_task(conn, task_id)
        
        if BackOffConfs.is_enabled:
            save_as_pickle(self.guardian_memory_task, "guardian_memory_task.pickle")
            save_as_pickle(self.guardian_memory_connector, "guardian_memory_connector.pickle")

        if not failed_connectors and not failed_tasks:
            logger.info("All tasks and connectors are "
                        "[green]healthy[/green] "
                        "[yellow]:)[/yellow]")
