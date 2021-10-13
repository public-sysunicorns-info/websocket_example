from pydantic import BaseModel, Field


class Device(BaseModel):
    device_id: str = Field(title="")
