from typing import TypedDict, Dict, List
from abc import ABC, abstractmethod

AWSAccountId = str
PermissionSetTypeDef = TypedDict(
    "PermissionSetTypeDef",
    {
        "Name": str,
        "Policy": Dict,
    },
    total=False,
)

class AppConfig(ABC):
    @abstractmethod
    def get_permission_sets(self) -> List[PermissionSetTypeDef]:
        raise NotImplementedError

    @abstractmethod
    def get_group_display_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_target_accounts(self) -> List[AWSAccountId]:
        raise NotImplementedError
