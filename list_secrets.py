import os
import boto3
from botocore.config import Config

def list_untagged_secrets(region=None, include_scheduled_for_deletion=False):
    sm = boto3.client("secretsmanager", region_name=region, config=Config(retries={"max_attempts": 10}))
    paginator = sm.get_paginator("list_secrets")

    untagged = []
    for page in paginator.paginate():
        for s in page.get("SecretList", []):
            # Skip secrets scheduled for deletion unless included
            if not include_scheduled_for_deletion and s.get("DeletedDate"):
                continue

            arn = s["ARN"]
            try:
                tags = s["Tags"]
            except KeyError:
                tags = None

            if not tags:
                untagged.append({"Name": s.get("Name"), "ARN": arn, "LastAccessedDate": s.get("LastAccessedDate")})

    return untagged

if __name__ == "__main__":
    # Set region if needed, e.g., region="us-east-1"
    aws_profile = os.environ["AWS_PROFILE"]
    results = list_untagged_secrets(region=None)
    for r in results:
        print(f'{aws_profile};{r["Name"]};{r["LastAccessedDate"]};{r["ARN"]}')
