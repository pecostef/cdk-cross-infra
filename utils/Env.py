import os
from dotenv import load_dotenv


class Env:
    _SSO_INSTANCE_ARN_VAR_NAME = "SSO_INSTANCE_ARN"
    _DEV_ACCOUNT_ID_VAR_NAME = "DEV_ACCOUNT_ID"
    _AWS_REGION_VAR_NAME = "AWS_REGION"
    _SSO_IDENTITY_STORE_ID_VAR_NAME = "SSO_IDENTITY_STORE_ID"
    _FAMILY_FOLDER_VAR_NAME = "FAMILY_FOLDER_NAME"

    def __init__(self):
        loaded = load_dotenv()
        if not loaded:
            print("Cannot load .env")
            return

    def get_sso_instance_arn(self) -> str:
        return os.getenv(Env._SSO_INSTANCE_ARN_VAR_NAME)

    def get_dev_account_id(self) -> str:
        return os.getenv(Env._DEV_ACCOUNT_ID_VAR_NAME)

    def get_aws_region(self) -> str:
        return os.getenv(Env._AWS_REGION_VAR_NAME)

    def get_sso_identity_store_id(self) -> str:
        return os.getenv(Env._SSO_IDENTITY_STORE_ID_VAR_NAME)

    def get_family_folder_name(self) -> str:
        return os.getenv(Env._FAMILY_FOLDER_VAR_NAME)
