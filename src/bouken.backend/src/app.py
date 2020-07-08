"""
Bouken backend API.

@author GalenS <galen.scovell@gmail.com>
"""

import os
import sys

from src.service.interior_map_generator import InteriorMapGenerator
from src.state.humidity import Humidity
from src.state.temperature import Temperature

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from src.util.logger import info, error
from src.model.responses import StatusResponse
from src.service.exterior_map_generator import ExteriorMapGenerator

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
    int_map_gen: InteriorMapGenerator = InteriorMapGenerator(
        pixel_width=900,
        pixel_height=720,
        cell_size=20,
        number_rooms=8,
        min_room_size=4,
        max_room_size=10,
        min_corridor_length=2,
        max_corridor_length=6,
    )

    # ext_map_gen: ExteriorMapGenerator = ExteriorMapGenerator(
    #     pixel_width=900,
    #     hex_size=10,
    #     initial_land_pct=0.3,
    #     required_land_pct=0.4,
    #     terraform_iterations=20,
    #     min_island_size=12,
    #     humidity=Humidity.Average,
    #     temperature=Temperature.Temperate,
    #     min_region_expansions=2,
    #     max_region_expansions=5,
    #     min_region_size_pct=0.0125
    # )

    # uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')
