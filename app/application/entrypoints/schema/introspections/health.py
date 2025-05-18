from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    status: str = Field(..., description="The status of the service.")
