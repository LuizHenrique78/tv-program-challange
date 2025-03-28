from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_program_data():
    response = client.get("/api/v1/program", params={"program_code": "HUCK", "date": "2020-07-25"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]['program_code'] == 'HUCK'
    assert data[0]['weekday'] == "Saturday"


def test_get_period_data():
    response = client.get("/api/v1/period",
                          params={"program_code": "HUCK", "start_date": "2022-07-25", "end_date": "2022-08-08"})

    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert all("available_time" in item for item in
               data)
    for item in data:
        assert item['program_code'] == 'HUCK'
        assert "weekday" in item


def test_get_program_data_no_data():
    response = client.get("/api/v1/program", params={"program_code": "HUCK", "date": "2022-07-25"})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No data found for this program and date"}


def test_get_period_data_no_data():
    response = client.get("/api/v1/period",
                          params={"program_code": "HUCK", "start_date": "2019-07-25", "end_date": "2019-08-08"})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No data found for the specified period"}
