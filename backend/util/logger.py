"""
Handles all logging for service.
"""

import colorlog
import logging.handlers
import sys
import traceback
import uvicorn


class Logger(object):
    def __init__(self) -> None:
        self.logger = logging.getLogger('Primary')
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        formatter = colorlog.ColoredFormatter('%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)


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
