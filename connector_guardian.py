import logging
from dotenv import load_dotenv
import os

from functionalities.connector_restart import ConnectorRestarter
from utils.rich_utils import MyRichLogHandler
from configs.config_validator import validate_backoff_configs

load_dotenv()

log_level = os.getenv("LOG_LEVEL",'info').upper()

base_log_format = ("%(asctime)s - %(levelname)s "
                   "in %(filename)s: "
                   "%(message)s")

logging.basicConfig(level=log_level,
                    format=base_log_format,
                    handlers=[MyRichLogHandler()])

validate_backoff_configs()
logging.info("Start [b green]Restarting[/b green] failed connectors")

ConnectorRestarter().restart_failed_connectors_and_tasks()