from typing import Dict


def generate_bucket_user_permissions(bucket_name: str, family_folder_name: str) -> Dict:
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["s3:GetBucketLocation", "s3:ListAllMyBuckets"],
                "Resource": "arn:aws:s3:::*",
                "Effect": "Allow",
                "Sid": "AllowUserToSeeBucketListInTheConsole",
            },
            {
                "Condition": {
                    "StringEquals": {
                        "s3:prefix": ["", "home/", "home/{aws:userid}"],
                        "s3:delimiter": ["/"],
                    },
                },
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{bucket_name}",
                "Effect": "Allow",
                "Sid": "AllowRootAndHomeListingOfFamilyBoxBucket",
            },
            {
                "Condition": {
                    "StringEquals": {
                        "s3:prefix": ["", "home/", f"home/{family_folder_name}"],
                        "s3:delimiter": ["/"],
                    },
                },
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{bucket_name}",
                "Effect": "Allow",
                "Sid": "AllowFamilyFolderListingOfFamilyBoxBucket",
            },
            {
                "Condition": {
                    "StringLike": {
                        "s3:prefix": ["home/{aws:userid}/*"],
                    },
                },
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{bucket_name}",
                "Effect": "Allow",
                "Sid": "AllowListingOfUserFolder",
            },
            {
                "Condition": {
                    "StringLike": {
                        "s3:prefix": [f"home/{family_folder_name}/*"],
                    },
                },
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{bucket_name}",
                "Effect": "Allow",
                "Sid": "AllowListingOfFamilyFolder",
            },
            {
                "Action": "s3:*",
                "Resource": f"arn:aws:s3:::{bucket_name}/home/{{aws:userid}}/*",
                "Effect": "Allow",
                "Sid": "AllowAllS3ActionsInUserFolder",
            },
            {
                "Action": "s3:*",
                "Resource": f"arn:aws:s3:::{bucket_name}/home/{family_folder_name}/*",
                "Effect": "Allow",
                "Sid": "AllowAllS3ActionsInFamilyFolder",
            },
        ],
    }
