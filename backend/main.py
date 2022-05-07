"""
Bouken backend API.

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

from backend.model.requests import ExteriorGenerateRequest
from backend.model.responses import StatusResponse
from backend.service.exterior_map_generator import ExteriorMapGenerator
from backend.service.interior_map_generator import InteriorMapGenerator
from backend.service.sqlite_service import SqliteService
from backend.state.humidity import Humidity
from backend.state.temperature import Temperature
from backend.util.logger import Logger


_log: Logger = Logger()
_db_service: SqliteService = SqliteService()
_exterior_map_generator: ExteriorMapGenerator = ExteriorMapGenerator(_log)
_interior_map_generator: InteriorMapGenerator = InteriorMapGenerator(_log)


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


def db_dependency() -> SqliteService:
    global _db_service
    if not _db_service:
        _db_service = None
    return _db_service


def _generate_response(status_code: int, contents: dict) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=jsonable_encoder(contents))


@app.get(
    path='/status',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Status',
    description='Get service status'
)
async def status(db=Depends(db_dependency)) -> JSONResponse:
    try:
        return _generate_response(200, {'status': 200})
    except Exception as ex:
        msg = {'message': 'Error checking service health'}
        _log.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.post(
    path='/generate/exterior',
    response_model=StatusResponse,
    status_code=HTTP_200_OK,
    summary='Generate an exterior map',
    description='Generate an exterior map'
)
async def create(req: ExteriorGenerateRequest, db=Depends(db_dependency)) -> JSONResponse:
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
        exterior_map: str = _exterior_map_generator.begin(
            req.pixel_width,
            req.hex_size,
            req.initial_land_pct,
            req.required_land_pct,
            req.terraform_iterations,
            req.min_island_size,
            req.humidity,
            req.temperature,
            req.min_region_expansions,
            req.max_region_expansions,
            req.min_region_size_pct
        )
        return _generate_response(200, {'map_str': exterior_map})
    except Exception as ex:
        msg = {'message': 'Error generating map'}
        _log.error(msg, ex)
        msg.update({'exception': ex.__str__()})
        return _generate_response(HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.on_event('shutdown')
def shutdown_event() -> None:
    _log.info('Service shutdown')


@app.on_event('startup')
def startup_event() -> None:
    _log.info('Service startup')
