from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response
import pytest


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
