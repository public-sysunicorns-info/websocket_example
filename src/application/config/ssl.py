from pydantic import BaseSettings, FilePath
from pydantic.fields import Field


class SSLConfig(BaseSettings):
    key_path: FilePath = Field(default=None)
    crt_path: FilePath = Field(default=None)
    ca_path: FilePath = Field(default=None)
