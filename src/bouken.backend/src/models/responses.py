"""
Defines all response models for the service.
"""

from pydantic import BaseModel
from typing import List


class StatusResponse(BaseModel):
    status: int


class NotReadyResponse(BaseModel):
    jobId: str
    message: str
    retryTimeMilliseconds: int


class ErrorResponse(BaseModel):
    message: str
