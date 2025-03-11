import pytest
import asyncio
from fastapi.testclient import TestClient

import main

client = TestClient(app=main.app)


@pytest.mark.asyncio
async def test_range_hours():
    """Test filtering energy data by date & time range"""

    response = await asyncio.to_thread(
        client.get,
        "/range?start_date=2022-02-01&start_hour=08:00:00&end_date=2022-02-02&end_hour=12:00:00",
    )

    assert response.status_code == 200, f"Failed with response: {response.text}"

    json_data = response.json()
    assert len(json_data["items"]) > 0, f"No data found for the given range"
    assert isinstance(json_data["items"][0]["date"], int), f"Date should be an integer"
    assert isinstance(
        json_data["items"][0]["consommation"], int
    ), f"Consommation should be an integer"
