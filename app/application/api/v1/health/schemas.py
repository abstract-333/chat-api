from typing import Literal

from pydantic import BaseModel


class HealthDetail(BaseModel):
    mongodb: str


class HealthOut(BaseModel):
    status: Literal["Ok", "MongoDB is down"]
    detail: HealthDetail
