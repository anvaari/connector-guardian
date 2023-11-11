import pickle 
import os 
import pathlib
import logging
from typing import Union
from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv('LOG_LEVEL','info').upper()
script_path=os.path.dirname(os.path.abspath(__file__))
project_path = str(pathlib.Path(script_path).parent.absolute())

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

def save_as_pickle(python_object:Union[list,dict,tuple],file_name:str) -> None:
    with open(os.path.join(project_path,file_name),'wb') as fp:
        try:
            pickle.dump(python_object,fp)
        except Exception as e:
            logger.error(f"Can't save {file_name} "
                         f"file as picke.\n{e}",exc_info=True)
        else:
            logger.debug("Save picke file successfully")

def load_dict_pickle(file_name:str) -> dict:
    if not os.path.isfile(os.path.join(project_path,file_name)):
        return dict()
    with open(os.path.join(project_path,file_name),'wb') as fp:
        try:
            python_object = pickle.load(fp)
        except Exception as e:
            logger.error(f"Can't load {file_name} "
                         f"file as picke, empty dict "
                         "will be returned.\n{e}",exc_info=True)
            return dict()
        else:
            logger.debug("picke file loaded successfully")
            return python_object