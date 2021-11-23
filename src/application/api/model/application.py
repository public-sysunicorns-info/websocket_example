from pydantic import BaseModel
from typing import List
from datetime import datetime

from application.service.device.model import Application

class ApplicationListResponse(BaseModel):
    application_list: List[Application]
