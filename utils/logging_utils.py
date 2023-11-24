import logging
import os
from dotenv import load_dotenv

load_dotenv("../.env")

def get_validated_log_level(default_level='INFO'):
    valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    log_level = os.getenv('LOG_LEVEL', default_level).upper()
    return log_level if log_level in valid_log_levels else default_level

def setup_logger(logger_name, level='INFO'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, get_validated_log_level(level)))
    return logger