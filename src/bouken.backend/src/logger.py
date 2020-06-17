"""
Handles all logging for service.

@author GalenS <galen.scovell@payscale.com>
"""

import logging.handlers
import sys
import traceback


logger = logging.getLogger('Primary')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def info(msg):
    """
    Write info message.
    """
    logger.info(msg)


def warn(msg, ex=None):
    """
    Write warning message (with stacktrace if exception is passed).
    """
    if ex:
        msg.update({'exception': _format_traceback(ex)})
    logger.warning(msg)


def error(msg, ex=None):
    """
    Write error message (with stacktrace if exception is passed).
    """
    if ex:
        msg.update({'exception': _format_traceback(ex)})
    logger.error(msg)


def _format_traceback(e):
    return ''.join(traceback.format_tb(e.__traceback__)).strip()
