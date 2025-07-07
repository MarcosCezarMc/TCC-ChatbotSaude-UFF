import os
import logging
from dotenv import load_dotenv

load_dotenv()

class CustomFormatter(logging.Formatter):
    def format(self, record):
        return f'[{record.levelname}] {record.getMessage()}'

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger = logging.getLogger()
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)

def get_must_have_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        logging.error(f"{var_name} não foi definido nas variáveis de ambiente")
        exit(1)
    return value