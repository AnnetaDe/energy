import pandas as pd
from sqlalchemy import insert
import asyncio


from helpers_db.timer_for_execution import time_it
from models import Energy_2, Energy_3
from session import get_session
from parse_excel_2_col import parse_folder_2_col


REQUIRED_COLUMNS_NEW: set[str] = {"id", "consommation"}
df = parse_folder_2_col(r"data_from_web", r"data_added")


def check_df(df: pd.DataFrame):
    """Checks if the DataFrame is empty and contains the required columns"""
    if df.empty:
        print("⚠️ No new data found. Skipping insertion.")
        raise ValueError("DataFrame is empty")

    if not REQUIRED_COLUMNS_NEW.issubset(df.columns):
        raise ValueError(
            f"Missing required columns: {REQUIRED_COLUMNS_NEW - set(df.columns)}"
            f"\nColumns found: {df.columns}"
        )

    return df


async def row_insert(df):
    """Inserts data row by row"""
    try:
        df = check_df(df)
    except ValueError as error:
        print(error)
        return

    async for session in get_session():
        for i in range(0, len(df)):
            stmt = insert(Energy_2).values(
                id=df.iloc[i]["id"], consommation=df.iloc[i]["consommation"]
            )
            await session.execute(stmt)
            await session.commit()
            print(f"✅ Inserted row {i + 1} ({len(df)} rows)")


async def bulk_insert(df, batch_size=1000):
    """Inserts data in batches of size batch_size. Default is 1000"""
    try:
        df = check_df(df)
    except ValueError as error:
        print(error)
        return

    async for session in get_session():
        BATCH_SIZE = 1000
        entries = [
            {
                "id": row["id"],
                "consommation": row["consommation"],
            }
            for _, row in df.iterrows()
        ]

        for i in range(0, len(entries), BATCH_SIZE):
            batch = entries[i : i + BATCH_SIZE]  # 1000 rec in one drop
            stmt = insert(Energy_3).values(batch)

            await session.execute(stmt)
            await session.commit()
            print(f"✅ Inserted batch {i // BATCH_SIZE + 1} ({len(batch)} rows)")


row_vs_bulk = {"row_insertion": row_insert, "batch_insertion": bulk_insert}


@time_it
def run_insertion_method(method_name: str, df: pd.DataFrame):
    """Runs the insertion method"""
    asyncio.run(row_vs_bulk[method_name](df))


# run_insertion_method("batch_insertion", df)
# ✅ Moved 2021.xlsx to data_added\2021.xlsx
# ✅ Inserted batch 1 (1000 rows)
# ✅ Inserted batch 2 (1000 rows)
# ✅ Inserted batch 3 (1000 rows)
# ✅ Inserted batch 4 (1000 rows)
# ✅ Inserted batch 2 (1000 rows)
# ✅ Inserted batch 3 (1000 rows)
# ✅ Inserted batch 4 (1000 rows)
# ✅ Inserted batch 3 (1000 rows)
# ✅ Inserted batch 4 (1000 rows)
# ✅ Inserted batch 4 (1000 rows)
# ✅ Inserted batch 5 (1000 rows)
# ✅ Inserted batch 5 (1000 rows)
# ✅ Inserted batch 6 (1000 rows)
# ✅ Inserted batch 7 (1000 rows)
# ✅ Inserted batch 8 (1000 rows)
# ✅ Inserted batch 9 (1000 rows)
# ✅ Inserted batch 10 (1000 rows)
# ✅ Inserted batch 11 (1000 rows)
# ✅ Inserted batch 12 (1000 rows)
# ✅ Inserted batch 13 (1000 rows)
# ✅ Inserted batch 14 (1000 rows)
# ✅ Inserted batch 15 (1000 rows)
# ✅ Inserted batch 16 (1000 rows)
# ✅ Inserted batch 17 (1000 rows)
# ✅ Inserted batch 18 (520 rows)
# ⏱️ Time taken: 5.72 seconds

# run_insertion_method("row_insertion", df)
# ✅ Inserted row 17520 (17520 rows)
# ⏱️ Time taken: 1536.55 seconds
