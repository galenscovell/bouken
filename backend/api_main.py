"""
Entrypoint for Bouken API.

@author GalenS <galen.scovell@gmail.com>
"""

import os
import sys

# This line is required for absolute imports to work throughout the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from model.requests import CreateExteriorRequest, CreateInteriorRequest
from model.responses import StatusResponse
from service.read_thru_cache.i_read_thru_cache import IReadThruCache
from service.read_thru_cache.gcp_read_thru_cache import GCPReadThruCache
from service.queue.i_queue import IQueue
from service.queue.gcp_queue import GCPQueue
from util.i_logger import ILogger
from util.logger import Logger

_logger: ILogger = Logger()
_cache: IReadThruCache
_queue: IQueue

app = FastAPI(
    title='Bouken API',
    description='',
    version='0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5050", "localhost:5050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def cache_dependency() -> IReadThruCache:
    global _cache
    if not _cache:
        _cache = GCPReadThruCache(_logger)
    return _cache


def queue_dependency() -> IQueue:
    global _queue
    if not _queue:
        _queue = GCPQueue(_logger)
    return _queue


def _generate_response(status_code: int, contents: dict) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=jsonable_encoder(contents))


@app.get(
    path='/status',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Status',
    description='Get service and dependencies status'
)
async def status(cache: IReadThruCache = Depends(cache_dependency)) -> JSONResponse:
    try:
        cache.ping()
        return _generate_response(200, {'status': 200})
    except Exception as ex:
        msg = {'message': 'Error checking service health'}
        _logger.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.post(
    path='/exterior',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Generate an exterior map',
    description='Generate an exterior map'
)
async def create_exterior(req: CreateExteriorRequest,
                          cache: IReadThruCache = Depends(cache_dependency),
                          queue: IQueue = Depends(queue_dependency)) -> JSONResponse:
    try:
        return _generate_response(200, {'map_guid': ''})
    except Exception as ex:
        msg = {'message': 'Error generating exterior map'}
        _logger.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.get(
    path='/exterior/{user_guid}/{map_guid}',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Get an exterior map',
    description='Get an exterior map'
)
async def get_exterior(user_guid: str,
                       map_guid: str,
                       cache: IReadThruCache = Depends(cache_dependency)) -> JSONResponse:
    pass


@app.post(
    path='/interior',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Generate an interior map',
    description='Generate an interior map'
)
async def create_interior(req: CreateInteriorRequest,
                          cache: IReadThruCache = Depends(cache_dependency),
                          queue: IQueue = Depends(queue_dependency)) -> JSONResponse:
    try:
        # interior_map: str = _interior_map_generator.begin(
        #     pixel_width=900,
        #     pixel_height=720,
        #     cell_size=20,
        #     number_rooms=8,
        #     min_room_size=4,
        #     max_room_size=10,
        #     min_corridor_length=2,
        #     max_corridor_length=6,
        # )
        return _generate_response(200, {'map_guid': ''})
    except Exception as ex:
        msg = {'message': 'Error generating interior map'}
        _logger.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.get(
    path='/interior/{user_guid}/{map_guid}',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Get an interior map',
    description='Get an interior map'
)
async def get_interior(user_guid: str,
                       map_guid: str,
                       cache: IReadThruCache = Depends(cache_dependency)) -> JSONResponse:
    pass


@app.on_event('shutdown')
def shutdown_event() -> None:
    _logger.info('Service shutdown')


@app.on_event('startup')
def startup_event() -> None:
    _logger.info('Service startup')
