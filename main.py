from contextlib import asynccontextmanager
from datetime import datetime, date
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.database import init_db
from app.models import Energy
from app.session import get_session
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        print("🚀 Database initialized.")
        yield
    finally:
        print("🛑 Closing database connection.")
        await app.state.db_engine.dispose()
        print("👋 Database connection closed.")


origins = ["*"]

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def health():
    return {"status": "Welcome to the API for energy consumption data."}


@app.get("/get_energy")
async def get_energy(session: AsyncSession = Depends(get_session)):
    stmt = select(Energy)
    results = await session.execute(stmt)
    all_entries = results.scalars().all()
    return all_entries


# curl -X 'GET' "http://127.0.0.1:8000/range?start=2022-02-01&end=2022-02-10"      -H "accept: application/json"


@app.get("/range_days")
async def get_energy_in_range(
    start: str, end: str, session: AsyncSession = Depends(get_session)
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = date.fromisoformat(end)
        print(f"Start: {start_date}, End: {end_date}")

        stmt = select(Energy).where(Energy.date.between(start_date, end_date))

        results = await session.execute(stmt)
        entries = results.scalars().all()

        return {
            "count": len(entries),
            "data": [
                {
                    "date": entry.date,
                    "heures": entry.heures,
                    "consommation": entry.consommation,
                }
                for entry in entries
            ],
            "total": sum([entry.consommation for entry in entries]),
        }
    except Exception as e:
        return {"error": str(e)}


# curl -X 'GET' "http://127.0.0.1:8000/range?start_date=2022-02-01&start_hour=08:00:00&end_date=2022-02-02&end_hour=12:00:00" \
#      -H "accept: application/json"
@app.get("/range")
async def get_energy_in_range_h(
    start_date: str,
    end_date: str,
    start_hour: str = "00:00:00",
    end_hour: str = "23:59:59",
    session: AsyncSession = Depends(get_session),
):
    try:
        start_day = datetime.strptime(start_date, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_hour, "%H:%M:%S").time()
        end_day = datetime.strptime(end_date, "%Y-%m-%d").date()
        end_time = datetime.strptime(end_hour, "%H:%M:%S").time()

        print(f"Filtering from {start_day} {start_time} to {end_day} {end_time}")

        # ✅ Handle single-day range
        if start_day == end_day:
            stmt = select(Energy).where(
                and_(
                    Energy.date == start_day,
                    Energy.heures.between(start_time, end_time),
                )
            )
        else:
            stmt = select(Energy).where(
                or_(
                    and_(Energy.date == start_day, Energy.heures >= start_time),
                    and_(Energy.date > start_day, Energy.date < end_day),
                    and_(Energy.date == end_day, Energy.heures <= end_time),
                )
            )

        results = await session.execute(stmt)
        entries = results.scalars().all()

        return {
            "count": len(entries),
            "data": [
                {
                    "date": entry.date,
                    "heures": entry.heures,
                    "consommation": entry.consommation,
                }
                for entry in entries
            ],
            "total": sum(entry.consommation for entry in entries),
        }

    except Exception as e:
        return {"error": str(e)}
