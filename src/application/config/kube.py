from pydantic import BaseSettings
from pydantic.fields import Field
from pydantic.networks import IPvAnyAddress


class KubeConfigModel(BaseSettings):
    node_name: str = Field(env="K8S_NODE_NAME", default=None)
    pod_name: str = Field(env="K8S_POD_NAME", default=None)
    pod_ip: IPvAnyAddress = Field(env="K8S_POD_IP", default=None)
    pod_service_account_name: str = Field(env="K8S_POD_SERVICE_ACCOUNT", default=None)

class KubeServiceAccountModel(BaseSettings):
    certificate_authority: str = Field(default=None)
    namespace: str = Field(default=None)
    token: str = Field(default=None)
