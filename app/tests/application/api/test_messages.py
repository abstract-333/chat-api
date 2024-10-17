import pytest
from faker import Faker
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.asyncio
async def test_create_chat_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
) -> None:
    url = app.url_path_for("create_chat_handler")
    title: str = faker.text(max_nb_chars=30)
    response: Response = client.post(url=url, json={"title": title})
    assert response.is_success
    json_data = response.json()
    assert json_data["title"] == title


@pytest.mark.asyncio
async def test_create_chat_fail_text_too_long(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
) -> None:
    url = app.url_path_for("create_chat_handler")
    title: str = faker.text(max_nb_chars=500)

    response: Response = client.post(url=url, json={"title": title})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data["detail"]["error"]


@pytest.mark.asyncio
async def test_create_chat_fail_text_empty(
    app: FastAPI,
    client: TestClient,
) -> None:
    url = app.url_path_for("create_chat_handler")

    response: Response = client.post(url=url, json={"title": ""})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data["detail"]["error"]
