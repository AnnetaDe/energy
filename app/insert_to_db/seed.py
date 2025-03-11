import asyncio
from sqlalchemy import insert, text
from database import Base
from session import get_session
from app.insert_to_db.models_db import Energy

from app.insert_to_db.parse_excel import parse_folder
import pandas as pd


BATCH_SIZE = 1000
REQUIRED_COLUMNS = {"date", "heures", "consommation"}


df = parse_folder(r"data_from_web", r"data_added")


def check_df(df: pd.DataFrame):
    if df.empty:
        print("⚠️ No new data found. Skipping insertion.")
        raise ValueError("DataFrame is empty")

    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError(
            f"Missing required columns: {REQUIRED_COLUMNS - set(df.columns)}"
            f"\nColumns found: {df.columns}"
        )

    return df


async def add_data_to_db(df: pd.DataFrame):
    try:
        df = check_df(df)
    except ValueError as error:
        print(error)
        return

    async for session in get_session():

        entries = [
            {
                "date": row["date"],
                "heures": row["heures"],
                "consommation": row["consommation"],
            }
            for _, row in df.iterrows()
        ]

        for i in range(0, len(entries), BATCH_SIZE):
            batch = entries[i : i + BATCH_SIZE]  # 1000 rec in one drop
            stmt = insert(Energy).values(batch)

            await session.execute(stmt)
            await session.commit()
            print(f"✅ Inserted batch {i // BATCH_SIZE + 1} ({len(batch)} rows)")


# asyncio.run(add_data_to_db(df))
