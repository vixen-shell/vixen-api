import logging
from typing import TypedDict, List, Literal, Callable, Any

class Log(TypedDict):
    level: Literal['INFO', 'WARNING', 'ERROR']
    message: str

LogListener = Callable[[Log], Any]

class LogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        if len(Logger.log_cache) == Logger.cache_size:
            Logger.log_cache.pop(0)

        log: Log = {
            'level': record.levelname,
            'message': record.getMessage()
        }

        Logger.log_cache.append(log)

        for listener in Logger.log_listeners:
            listener(log)

class Logger:
    cache_size = 256
    log_cache: List[Log] = []
    log_listeners: List[LogListener] = []
    log_handler = LogHandler()


    @staticmethod
    def start():
        def addLoggerHandler(name: str):
            logger = logging.getLogger(name)
            logger.addHandler(Logger.log_handler)

        addLoggerHandler('uvicorn')
        addLoggerHandler('uvicorn.access')

    @staticmethod
    def log(level: Literal['INFO', 'WARNING', 'ERROR'], message: str):
        logger = logging.getLogger('uvicorn')

        if level == 'INFO': logger.info(message)
        if level == 'WARNING': logger.warning(message)
        if level == 'ERROR': logger.error(message)

    @staticmethod
    def add_log_listener(listener: LogListener):
        Logger.log_listeners.append(listener)

    @staticmethod
    def remove_log_listener(listener: LogListener):
        Logger.log_listeners.remove(listener)