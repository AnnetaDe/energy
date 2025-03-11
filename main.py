from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import (
    add_pagination,
    LimitOffsetPage,
    LimitOffsetParams,
)
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.insert_to_db.models_db import Energy, Energy_3
from app.database import init_db, async_session
from dotenv import load_dotenv

from app.schemas import Energy_3_schema
from app.session import get_session

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
        print("👋 Database connection closed!")


origins = ["*"]

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def health():
    return {"status": "Welcome to the API for energy consumption data."}


@app.get("/range", response_model=LimitOffsetPage[Energy_3_schema])
async def get_energy_in_range_h(
    start_date: str,
    end_date: str,
    start_hour: str = "00:00:00",
    end_hour: str = "23:59:59",
    limit: int = Query(12, ge=1),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    params: LimitOffsetParams = Depends(),
):
    try:

        start_str = f"{start_date} {start_hour}"
        end_str = f"{end_date} {end_hour}"
        start_datetime = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
        start_datetime = start_datetime.replace(tzinfo=timezone.utc)
        end_datetime = end_datetime.replace(tzinfo=timezone.utc)
        milliseconds_start = int(start_datetime.timestamp() * 1000)
        milliseconds_end = int(end_datetime.timestamp() * 1000)
        print(f"Start: {milliseconds_start}, End: {milliseconds_end}")

        small_stmt = select(Energy_3).where(
            Energy_3.date.between(milliseconds_start, milliseconds_end)
        )

        paginated_entries = await paginate(session, small_stmt, params=params)
        print(paginated_entries)
        print(LimitOffsetPage[Energy_3_schema])

        return paginated_entries

    except Exception as e:
        return {"error": str(e)}


add_pagination(app)
