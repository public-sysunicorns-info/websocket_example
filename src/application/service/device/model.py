from pydantic import BaseModel, Field
from datetime import datetime

class Device(BaseModel):
    device_id: str = Field(title="DeviceId")

class Application(BaseModel):
    name: str = Field(title="Application Name AutoGenerated")
    last_register: datetime = Field(title="Last Register HealthCheck of this application")
