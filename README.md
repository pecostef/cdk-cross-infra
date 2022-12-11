# Cross-infra CDK stacks

This project contains infrastructure setup that might be required by multiple applications and therefore cannot be placed in one of the application-specific stacks.

## SSO Stack

This stack creates permissions sets and permission set assignments resources in IAM Identity Center (previously known as AWS SSO). Since permissions are app-dependant, for each app, a configuration class must be implemented ([`AppConfig`](sso/appconfigs/AppConfig.py)) in order to:

- provide the desired policies
- provide the group display name in IAM Identity Center to which attach the policies
- provide the target account IDs which the permission sets should be enabled for

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation
