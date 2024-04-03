"""
Entrypoint for Bouken API.

@author GalenS <galen.scovell@gmail.com>
"""

import os
import sys

from util.biome_calculator import BiomeCalculator
from util.hex_utils import HexUtils

# This line is required for absolute imports to work throughout the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from model.requests import CreateExteriorRequest, CreateInteriorRequest
from model.responses import StatusResponse
from util.i_logger import ILogger
from util.logger import Logger

from service.generator.exterior_map_generator import ExteriorMapGenerator
from service.generator.interior_map_generator import InteriorMapGenerator

_logger: ILogger = Logger()
_biome_calculator = BiomeCalculator()
_hex_utils = HexUtils()
_exterior_map_generator: ExteriorMapGenerator = ExteriorMapGenerator(_logger, _biome_calculator, _hex_utils)
_interior_map_generator: InteriorMapGenerator = InteriorMapGenerator(_logger)

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


def _generate_response(status_code: int, contents: dict) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=jsonable_encoder(contents))


@app.get(
    path='/status',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Status',
    description='Get service and dependencies status'
)
async def status() -> JSONResponse:
    try:
        return _generate_response(200, {'status': 200})
    except Exception as ex:
        msg = {'message': 'Error checking service health'}
        _logger.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.post(
    path='/generate/exterior',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Generate an exterior map',
    description='Generate an exterior map'
)
async def create_exterior(req: CreateExteriorRequest) -> JSONResponse:
    try:
        _exterior_map_generator.instantiate(req)
        exterior_map_guid: str = ''
        if req.debug:
            _exterior_map_generator.debug_render()
            _exterior_map_generator.debug_save()
        else:
            exterior_map_guid = _exterior_map_generator.generate()
        return _generate_response(200, {'map_guid': exterior_map_guid})
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
async def get_exterior(user_guid: str, map_guid: str,) -> JSONResponse:
    pass


@app.post(
    path='/generate/interior',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Generate an interior map',
    description='Generate an interior map'
)
async def create_interior(req: CreateInteriorRequest) -> JSONResponse:
    try:
        _interior_map_generator.instantiate(req)
        interior_map_guid: str = ''
        if req.debug:
            _interior_map_generator.debug_render()
            # _interior_map_generator.debug_save()
        else:
            interior_map_guid = _interior_map_generator.generate()
        return _generate_response(200, {'map_guid': interior_map_guid})
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
async def get_interior(user_guid: str, map_guid: str) -> JSONResponse:
    pass


@app.on_event('shutdown')
def shutdown_event() -> None:
    _logger.info('Service shutdown')


@app.on_event('startup')
def startup_event() -> None:
    _logger.info('Service startup')
