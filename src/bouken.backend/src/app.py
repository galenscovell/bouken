"""
Bouken backend API.

@author GalenS <galen.scovell@gmail.com>
"""

import os
import sys
import uuid

import uvicorn

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from typing import List

from src.logger import info, warn, error
from src.models.responses import StatusResponse
from src.service.map_generator import MapGenerator

app = FastAPI(
    title='Bouken API',
    description='',
    version='0.1'
)

_db_service = None


def db_dependency():
    global _db_service
    if not _db_service:
        _db_service = None
    return _db_service


@app.on_event('shutdown')
def shutdown_event():
    info('Service shutdown')


@app.on_event('startup')
def startup_event():
    info('Service startup')


def _generate_response(status_code: int, contents: dict):
    return JSONResponse(status_code=status_code, content=jsonable_encoder(contents))


@app.get(
    path='/status',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Status',
    description='Get service status'
)
def status(db=Depends(db_dependency)):
    try:
        return _generate_response(200, {'status': 200})
    except Exception as ex:
        msg = {'message': 'Error checking service health'}
        error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.post(
    path='/',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Create map',
    description='Generate a new map'
)
def create(db=Depends(db_dependency)):
    try:
        return _generate_response(200, {})
    except Exception as ex:
        msg = {'message': 'Error generating map'}
        error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


if __name__ == '__main__':
    map_gen = MapGenerator()
    map_gen.generate_overworld(200, 200, 16, 3)
    # uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')
