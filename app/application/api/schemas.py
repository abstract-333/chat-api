from pydantic import BaseModel


class ErrorCodeSchema(BaseModel):
    error: str


class ErrorSchema(BaseModel):
    detail: ErrorCodeSchema
