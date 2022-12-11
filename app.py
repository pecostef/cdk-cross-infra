#!/usr/bin/env python3
import aws_cdk as cdk

from sso.appconfigs.FamilyboxConfig import FamilyboxConfig
from sso.sso_stack import SsoStack, SsoStackParamsTypeDef
from utils.Env import Env

env = Env()
app = cdk.App()
familybox_config = FamilyboxConfig(env=env)
sso_stack_params: SsoStackParamsTypeDef = {"Configs": [familybox_config]}

SsoStack(app, "SsoStack", env=env, params=sso_stack_params)

app.synth()
