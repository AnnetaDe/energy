from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

database_URL = os.getenv("DATABASE_URL")
if not database_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


Base = declarative_base()

engine = create_async_engine(
    database_URL,
    echo=False,
    future=True,
    pool_size=20,  # Larger base pool
    max_overflow=20,  # Allows up to 40 total
    pool_timeout=60,  # Wait up to 60s for a connection
)

async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db():
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
