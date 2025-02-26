from sqlalchemy import text
import asyncio

from session import get_session


async def get_entry_count():
    """Get the total number of entries in the 'energy' table."""
    async for session in get_session():
        result = await session.execute(text("SELECT COUNT(*) FROM energy"))
        count = result.scalar()
        print(f"Total entries: {count}")
        return count


asyncio.run(get_entry_count())
