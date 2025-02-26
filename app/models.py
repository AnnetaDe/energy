from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.orm import mapped_column

from .database import Base


class Energy(Base):
    __tablename__ = "energy"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    heures = Column(Time)
    consommation = Column(Integer)
