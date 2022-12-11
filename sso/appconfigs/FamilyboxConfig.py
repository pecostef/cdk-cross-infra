from typing import List
from sso.appconfigs.AppConfig import AWSAccountId, AppConfig, PermissionSetTypeDef
from sso.policies import generate_bucket_user_permissions
from sso.sso_stack import Env


class FamilyboxConfig(AppConfig):
    def __init__(self, env: Env) -> None:
        super().__init__()
        self.env = env

    def get_permission_sets(self) -> List[PermissionSetTypeDef]:
        return [
            PermissionSetTypeDef({
                "Name": "SSOFamilyBoxDevPermissionSet",
                "Policy": generate_bucket_user_permissions(
                    bucket_name="familybox-dev",
                    family_folder_name=self.env.get_family_folder_name(),
                ),
            })
        ]

    def get_group_display_name(self) -> str:
        return "FamilyBox"

    def get_target_accounts(self) -> List[AWSAccountId]:
        return [self.env.get_dev_account_id()]
