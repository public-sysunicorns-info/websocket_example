from pydantic import BaseModel, Field
from typing import List


class ErrorResponseModel(BaseModel):
    error_message: str = Field(
        default="An Error Occur", 
        description="Summarize the error")

