#!/bin/bash
. ./all_aws_profiles.sh

for AWS_PROFILE in $AWS_PROFILES; do
    account_name=$(aws account get-account-information --profile $AWS_PROFILE --query AccountName --output text)
    aws account get-alternate-contact --alternate-contact-type OPERATIONS --profile $AWS_PROFILE --output text | sed s/^/"$AWS_PROFILE"'	'"$account_name"'	'/|sed s/'	'/\;/g
done
