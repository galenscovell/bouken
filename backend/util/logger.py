"""
Handles all logging for service.
"""

import colorlog
import logging.handlers
import traceback
import uvicorn


class Logger:
    def __init__(self) -> None:
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter('%(log_color)s [%(asctime)s] (%(levelname)s) %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

        for logger in uvicorn.config.LOGGING_CONFIG['loggers']:
            uvicorn_logger = logging.getLogger(logger)
            uvicorn_logger.handlers.clear()
            uvicorn_logger.propagate = True


    def info(self, msg) -> None:
        """
        Write info message.
        """
        self.logger.info(msg)


    def warn(self, msg, ex=None) -> None:
        """
        Write warning message (with stacktrace if exception is passed).
        """
        if ex:
            msg.update({'exception': Logger._format_traceback(ex)})
        self.logger.warning(msg)


    def error(self, msg, ex=None) -> None:
        """
        Write error message (with stacktrace if exception is passed).
        """
        if ex:
            msg.update({'exception': Logger._format_traceback(ex)})
        self.logger.error(msg)


    @staticmethod
    def _format_traceback(e) -> str:
        return ''.join(traceback.format_tb(e.__traceback__)).strip()
