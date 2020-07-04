"""
Defines all request model for the service.
"""

from pydantic import BaseModel
from typing import List, Optional


class JobCreateRequest(BaseModel):
    appId: str
    accountId: str
    userId: str
    inputs: List
