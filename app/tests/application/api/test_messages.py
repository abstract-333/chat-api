from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
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


# @pytest.mark.asyncio
# async def test_create_message_success(
#     app: FastAPI,
#     client: TestClient,
#     faker: Faker,
#     chats_repository: BaseChatsRepository,
# ) -> None:
#     url = app.url_path_for("create_chat_handler")
#     title: str = faker.text(max_nb_chars=30)
#     response: Response = client.post(url=url, json={"title": title})
#     json_data = response.json()
#     chat_oid: str = json_data["oid"]
#     print(json_data["oid"])
#
#     assert await chats_repository.check_chat_exists_by_title(
#         title=title,
#     )
#     # TODO: Fix 404 chat not found, ever it was created...
#
#     url = app.url_path_for("create_message_handler", chat_oid=chat_oid)
#     message_text: str = faker.text(max_nb_chars=33)
#     response: Response = client.post(url=url, json={"text": message_text})
#     assert response.is_success
#     json_data = response.json()
#     assert json_data["text"] == message_text
