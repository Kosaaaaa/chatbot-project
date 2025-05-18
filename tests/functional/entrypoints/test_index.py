from http import HTTPStatus

from httpx import AsyncClient


async def test_index(test_client: AsyncClient) -> None:
    response = await test_client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == "text/html; charset=utf-8"
