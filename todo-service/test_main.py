from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    
def test_create_todo_success(mocker):
    # Giả lập httpx.get() luôn trả về response giả với status_code 200
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch("main.httpx.get", return_value=mock_response)

    response = client.post("/todos", json={
        "title": "Hoc pytest",
        "description": "Viet test cho todo-service",
        "user_id": 1
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Hoc pytest"
    assert data["user_id"] == 1
    assert data["completed"] is False
    
def test_create_todo_user_not_found(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch("main.httpx.get", return_value=mock_response)

    response = client.post("/todos", json={
        "title": "Todo cho user khong ton tai",
        "user_id": 999
    })

    assert response.status_code == 400
    assert "khong ton tai" in response.json()["detail"]