import requests
import logging
from dotenv import load_dotenv
import os 
from typing import Union
from utils.request_utils import send_request
from exceptions.custom_exceptions import RequestFailedError

load_dotenv()

log_level = os.getenv('LOG_LEVEL','info').upper()
connect_host = os.getenv("KAFKA_CONNECT_HOST","localhost")
connect_protocol = os.getenv("KAFKA_CONNECT_PROTOCOL",'http')
connect_port = os.getenv("KAFKA_CONNECT_PORT","8083")
connect_user = os.getenv("KAFKA_CONNECT_USER","")
connect_pass = os.getenv("KAFKA_CONNECT_PASS","")

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

base_connect_url = f"{connect_protocol}://{connect_host}:{connect_port}"


def get_connectors_status(connector_name:str) -> Union[dict[str,str],None]:
    status_url = base_connect_url + "/connectors?expand=status"
    try:
        res = send_request(status_url,
                           connect_user,
                           connect_pass)
    except RequestFailedError:
        logger.error("Can't get status for connectors. "
                     "Check the logs for more info")
        return None
    else:
        full_status = res.json()

        connectors_status = dict()
        for k,v in full_status.items():
            new_v = {
                'connector':v['status']['connector']['state'],
                'tasks':{i['id']:i['state'] for i in v['status']['tasks']} 
            }
            connectors_status[k] = new_v
        
        return connectors_status