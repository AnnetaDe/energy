from pydantic import BaseModel
from datetime import date, time


class Energy_schema(BaseModel):
    date: str
    heures: str
    consommation: int
