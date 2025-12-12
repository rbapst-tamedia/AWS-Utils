#!/bin/bash
. ./all_aws_profiles.sh

for AWS_PROFILE in $AWS_PROFILES; do
    account_name=$(aws account get-account-information --profile $AWS_PROFILE --query AccountName --output text)
    account_aliases=$(aws iam list-account-aliases --profile $AWS_PROFILE --query AccountAliases --output text)
    #aws account get-alternate-contact --alternate-contact-type OPERATIONS --profile $AWS_PROFILE --output text | sed s/^/"$AWS_PROFILE"'	'"$account_name"'	'/|sed s/'	'/\;/g

    echo $account_name $account_aliases

done
