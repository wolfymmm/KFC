import pytest
import mongomock
from react import app as flask_app
import react as meter_app

@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    mock_client = mongomock.MongoClient()
    db = mock_client["dual-zone-meter"]
    meter_app.readings_collection = db["meter_readings"]
    meter_app.meters_collection = db["meters"]
    yield

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def submit_reading(client, meter_id, day, night):
    return client.post(f"/?meter_id={meter_id}", data={
        "day": str(day),
        "night": str(night)
    }, follow_redirects=True)

def test_new_meter_reading(client):
    meter_id = "M001"
    response = submit_reading(client, meter_id, 120, 80)
    assert b"\xd0\x94\xd0\xb0\xd0\xbd\xd1\x96 \xd1\x83\xd1\x81\xd0\xbf\xd1\x96\xd1\x88\xd0\xbd\xd0\xbe \xd0\xb4\xd0\xbe\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xbe!" in response.data
    readings = list(meter_app.readings_collection.find({"meter_id": meter_id}))
    assert len(readings) == 1
    assert readings[0]["day"] == 120
    assert readings[0]["night"] == 80

def test_existing_meter_reading(client):
    meter_id = "M001"
    submit_reading(client, meter_id, 100, 70)
    response = submit_reading(client, meter_id, 150, 90)
    readings = list(meter_app.readings_collection.find({"meter_id": meter_id}))
    assert len(readings) == 2
    assert readings[-1]["delta_day"] == 50
    assert readings[-1]["delta_night"] == 20

def test_underreported_night(client):
    meter_id = "M002"
    submit_reading(client, meter_id, 100, 100)
    response = submit_reading(client, meter_id, 120, 90)
    latest = list(meter_app.readings_collection.find({"meter_id": meter_id}))[-1]
    assert latest["delta_night"] == 80  # накрутка
    assert latest["night"] == 180

def test_underreported_day(client):
    meter_id = "M003"
    submit_reading(client, meter_id, 100, 100)
    response = submit_reading(client, meter_id, 90, 120)
    latest = list(meter_app.readings_collection.find({"meter_id": meter_id}))[-1]
    assert latest["delta_day"] == 100  # накрутка
    assert latest["day"] == 200

def test_underreported_day_and_night(client):
    meter_id = "M003"
    submit_reading(client, meter_id, 200, 200)
    response = submit_reading(client, meter_id, 150, 100)
    latest = list(meter_app.readings_collection.find({"meter_id": meter_id}))[-1]
    assert latest["day"] == 300
    assert latest["night"] == 280
    assert latest["delta_day"] == 100
    assert latest["delta_night"] == 80
