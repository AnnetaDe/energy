from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date, datetime, time, timezone
from typing import Annotated, Optional


class Energy_schema(BaseModel):
    date: str
    heures: str
    consommation: int


class Energy_3_schema(BaseModel):

    consommation: int
    date: int
