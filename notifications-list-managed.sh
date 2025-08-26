#!/bin/bash
. ./all_aws_profiles.sh

#aws notifications list-managed-notification-channel-associations --region us-east-1 --managed-notification-configuration-arn arn:aws:notifications::911453050078:
# Get the AWS-Health Configuration.
# $ aws notifications list-managed-notification-configurations --region us-east-1
# {
#     "managedNotificationConfigurations": [
#         {
#             "arn": "arn:aws:notifications::911453050078:managed-notification-configuration/category/AWS-Health/sub-category/Security",
#             "name": "Security",
#             "description": "Health events with Security implications that are sent through email. By default, these are sent to the root email address, operations alternate contact, and the security alternate contact."
#         },
#         {
#             "arn": "arn:aws:notifications::911453050078:managed-notification-configuration/category/AWS-Health/sub-category/Operations",
#             "name": "Health Operations",
#             "description": "Health events with Operational implications that are sent through email. By default, these are sent to the root email address and the operations alternate contact."
#         },
#         {
#             "arn": "arn:aws:notifications::911453050078:managed-notification-configuration/category/AWS-Health/sub-category/Issue",
#             "name": "Account-Specific Issues",
#             "description": "All account-specific Health events that do not send emails by default. These Health events provide frequent updates about the state of your AWS infrastructure, such as service events or maintenance notices."
#         },
#         {
#             "arn": "arn:aws:notifications::911453050078:managed-notification-configuration/category/AWS-Health/sub-category/Billing",
#             "name": "Billing Notification",
#             "description": "Health events with Billing implications that are sent through email. By default, these are sent to the root email address, operations alternate contact, and the billing alternate contact."
#         }
#     ]
# }
#
# We're interested in the "Operations" sub-category. List if it's enabled
AWS_PROFILES="
dai_sandbox-admin
disco_dev-admin
"
for AWS_PROFILE in $AWS_PROFILES; do
    account_name=$(aws account get-account-information --profile $AWS_PROFILE --query AccountName --output text)
    account_id=$(aws sts get-caller-identity --query Account --output text)
    for sub_category in Operations Issue; do
        config_arn=arn:aws:notifications::$account_id:managed-notification-configuration/category/AWS-Health/sub-category/$sub_category
        aws notifications list-managed-notification-channel-associations --region us-east-1 --profile $AWS_PROFILE --managed-notification-configuration-arn $config_arn --query 'channelAssociations[]|[?channelIdentifier==`ACCOUNT_ALTERNATE_OPERATIONS`]' --output text | sed s/^/"$AWS_PROFILE"'	'"$account_name"'	'"$sub_category"'	'/|sed s/'	'/\;/g
    done
done
