from pydantic import BaseModel, Field
import enum

from application.service.device.model import Device

class EventStatus(str, enum.Enum):
    OK = "OK"
    ERROR = "ERROR"

class EventModelResponse(BaseModel):
    device: Device
    event_status: EventStatus
