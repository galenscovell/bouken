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

from src.logger import info, warn, error
from src.models.responses import StatusResponse

app = FastAPI(
    title='Bouken API',
    description='',
    version='0.1'
)

_backend = None


def backend_dependency():
    global _backend
    if not _backend:
        _backend = None
    return _backend


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
def status(backend=Depends(backend_dependency)):
    try:
        backend_status = backend.status()
        return _generate_response(backend_status, {'status': backend_status})
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
def create(backend=Depends(backend_dependency)):
    try:
        # BaseURL: https://www.dnd5eapi.co/api
        # These all return summarized entries with an index that must be passed back in for detail
        # GET /monsters, /classes, /ability-scores, /proficiencies, /skills, /races, /subraces,
        # /subraces/{index}/traits, /equipment, /spells, /conditions, /languages, /magic-schools,
        # /damage-types, /weapon-properties, /equipment-categories, /starting-equipment, /spellcasting,
        # /features, /subclasses

        backend_status = backend.status()
        return _generate_response(backend_status, {'status': backend_status})
    except Exception as ex:
        msg = {'message': 'Error generating map'}
        error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')
