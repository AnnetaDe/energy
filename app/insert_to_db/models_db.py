from sqlalchemy import Column, Integer, Date, Time, Numeric

from app.database import Base


class Energy(Base):
    __tablename__ = "energy"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    heures = Column(Time)
    consommation = Column(Integer)


class Energy_2(Base):
    __tablename__ = "energy_2"

    date = Column(Numeric, primary_key=True, index=True)
    consommation = Column(Numeric)


class Energy_3(Base):
    __tablename__ = "energy_3"

    date = Column(Numeric, primary_key=True, index=True)
    consommation = Column(Numeric)

    def __repr__(self):
        return f"{self.date}---> {self.consommation}"
