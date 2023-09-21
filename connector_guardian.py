import logging
from dotenv import load_dotenv
import os
from rich.logging import RichHandler
from functionalities.connector_restart import restart_failed_connectors_and_tasks

load_dotenv()

log_level = os.getenv("LOG_LEVEL",'info').upper()

base_log_format = ("%(asctime)s - %(levelname)s "
                   "in file %(filename)s function "
                   "%(funcName)s line %(lineno)s : "
                   "%(message)s")

logging.basicConfig(level=log_level,
                    format=base_log_format,
                    handlers=[RichHandler(markup=True)])

logging.info("Start [b green]Restarting[/b green] failed connectors")

restart_failed_connectors_and_tasks()