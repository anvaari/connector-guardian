import requests
import logging
from dotenv import load_dotenv
import os 
from exceptions.custom_exceptions import RequestFailedError

load_dotenv()

log_level = os.getenv("LOG_LEVEL",'info').upper()

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

def send_request(url:str,
                 method:str,
                 username:str="",
                 password:str="",
                 retry_count:int=3) -> requests.Response:
    rest_methods = ['get','put','post','delete','patch']
    if method.lower() not in rest_methods:
        raise ValueError("Inappropriate method provided. "
                         f"It's {method} but should be one of {rest_methods}")
    logger.debug(f"Start sending request to {url}")
    for i in range(retry_count):
        logger.debug(f"Request {i+1} of {retry_count}")
        try:
            with requests.Session() as session:
                if username and password:
                    session.auth = (username, password)
                
                request_method = getattr(session,method.lower())
                response = request_method(url)

                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error:\n{e}",exc_info=True)
        else:
            logger.debug("Successfully got respond "
                             f"from {url}")
            return response

    raise RequestFailedError(url)