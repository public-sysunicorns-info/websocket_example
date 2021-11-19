from pydantic import BaseModel
from typing import List
from application.service.device.model import Device


class DeviceListModel(BaseModel):
    devices: List[Device]
