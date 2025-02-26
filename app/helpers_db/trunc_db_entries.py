from sqlalchemy import text
import asyncio

from session import get_session


async def delete_all_entries():
    """Delete all rows from the 'energy' table."""
    async for session in get_session():
        await session.execute(text("DELETE FROM energy"))
        await session.commit()
        print("✅ All entries deleted successfully!")
