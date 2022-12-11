from typing import Dict, List, TypedDict

import boto3
from aws_cdk import Stack, aws_sso
from constructs import Construct
from mypy_boto3_identitystore.type_defs import GroupTypeDef

from sso.appconfigs.AppConfig import AppConfig
from utils.Env import Env

client = boto3.client("identitystore")

SsoStackParamsTypeDef = TypedDict("SsoStackParamsTypeDef", {"Configs": List[AppConfig]})


class SsoStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: Env,
        params: SsoStackParamsTypeDef,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.env = env
        for app_config in params["Configs"]:
            self._create_sso_resources_for_app(app_config)

    def _create_sso_resources_for_app(self, config: AppConfig):
        self._permission_set_arns: List[str] = []
        group_name = config.get_group_display_name()
        group: GroupTypeDef = find_by_group_display_name(
            group_name, self.env.get_sso_identity_store_id()
        )
        if group != None:
            self._create_permission_sets(group=group, app_config=config)
        else:
            print("group not found, no permissions will be created")

    def _create_permission_sets(self, group: GroupTypeDef, app_config: AppConfig):
        for permission in app_config.get_permission_sets():
            ps = self._create_permission_set_resource(
                name=permission["Name"],
                policy=permission["Policy"],
                instance_arn=self.env.get_sso_instance_arn(),
            )
            self._permission_set_arns.append(ps.attr_permission_set_arn)

        for account_id in app_config.get_target_accounts():
            for arn in self._permission_set_arns:
                self._create_permission_set_group_assignment_resource(
                    instance_arn=self.env.get_sso_instance_arn(),
                    group_name=group["DisplayName"],
                    group_id=group["GroupId"],
                    perm_set_arn=arn,
                    target_account_id=account_id,
                )

    def _create_permission_set_resource(
        self, name: str, policy: Dict, instance_arn: str
    ) -> aws_sso.CfnPermissionSet:
        return aws_sso.CfnPermissionSet(
            scope=self,
            id=name,
            name=name,
            instance_arn=instance_arn,
            inline_policy=policy,
        )

    def _create_permission_set_group_assignment_resource(
        self,
        instance_arn: str,
        group_id: str,
        group_name: str,
        perm_set_arn: str,
        target_account_id: str,
    ):
        return aws_sso.CfnAssignment(
            id=f"{group_name}Assignment",
            scope=self,
            instance_arn=instance_arn,
            principal_id=group_id,
            principal_type="GROUP",
            permission_set_arn=perm_set_arn,
            target_id=target_account_id,
            target_type="AWS_ACCOUNT",
        )


def find_by_group_display_name(
    group_display_name: str, identity_store_id: str
) -> GroupTypeDef:
    groups: List[GroupTypeDef] = []
    data = client.list_groups(IdentityStoreId=identity_store_id)
    if data["Groups"]:
        groups = data["Groups"]
    while "NextToken" in data and data["NextToken"] is not None:
        data = client.list_groups(
            IdentityStoreId=identity_store_id, NextToken=data["NextToken"]
        )
        if data["Groups"] is not None:
            groups.append(data["Groups"])

    group: GroupTypeDef = filter(
        lambda g: g["DisplayName"] == group_display_name, groups
    )
    return next(group, None)
