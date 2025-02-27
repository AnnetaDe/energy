import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_range_hours():
    """Test filtering energy data by date & time range"""

    response = await asyncio.to_thread(
        client.get,
        "/range?start_date=2022-02-01&start_hour=08:00:00&end_date=2022-02-02&end_hour=12:00:00",
    )

    assert response.status_code == 200, f"Failed with response: {response.text}"

    json_data = response.json()

    assert "count" in json_data, f"Unexpected response: {json_data}"
    assert "data" in json_data
    assert "total" in json_data

    if json_data["count"] > 0:
        sample = json_data["data"][0]
        assert "date" in sample
        assert "heures" in sample
        assert "consommation" in sample
