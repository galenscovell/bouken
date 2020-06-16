"""
Entrypoint for the service.

@author GalenS <galen.scovell@payscale.com>
"""

import os
import sys

import uuid
import uvicorn

from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from src.logger import info, warn, error, setup_logging


app = FastAPI(
    title='',
    description='',
    version='0.1'
)


def _generate_response(status_code: int, contents: dict):
    return JSONResponse(status_code=status_code, content=jsonable_encoder(contents))


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')