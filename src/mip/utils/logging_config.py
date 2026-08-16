'''
Centralized logging configuration for the MIP CLI.

Called exactly once , from cli/main/py( the composition root).
All other modules should only even call 'logging.getLogger(__name__)'
and never configure handlers themselves.
'''

import logging
from logging.config import dictConfig


def configure_logging(level:int = logging.INFO) -> None :

    '''Configure the root logger using dictConfig'''

    logging_config = {
        "version" : 1 , 
        "disable_existing_loggers" : False , 
        "formatters" : {
            "default" : {
                "format" : "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
            },
        },
        "handlers" : {
            "console": {
                "class":"logging.StreamHandler" , 
                "formatter" : "default" , 
                "level" : level
            },
        },
        "root" : {
            "handlers" : ["console"] , 
            "level" : level
        } , 
    }
    dictConfig(logging_config)


   