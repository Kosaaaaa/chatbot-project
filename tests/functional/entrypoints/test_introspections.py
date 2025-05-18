from http import HTTPStatus

from httpx import AsyncClient

from app.application.entrypoints.schema.introspections.health import HealthCheck


async def test_check_health(test_client: AsyncClient) -> None:
    response = await test_client.get("/introspections/health")

    assert response.status_code == HTTPStatus.OK

    parsed_response = HealthCheck.model_validate(response.json())

    assert parsed_response.status == "healthy"
