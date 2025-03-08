from sqlalchemy import Column, Integer, String, Date, Time, Numeric
from sqlalchemy.orm import mapped_column

from .database import Base


class Energy(Base):
    __tablename__ = "energy"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    heures = Column(Time)
    consommation = Column(Integer)


class Energy_2(Base):
    __tablename__ = "energy_2"

    id = Column(Numeric, primary_key=True, index=True)
    consommation = Column(Numeric)


class Energy_3(Base):
    __tablename__ = "energy_3"

    id = Column(Numeric, primary_key=True, index=True)
    consommation = Column(Numeric)
