#!/bin/bash
# Download waf rules
filenamePrefix=${1:-$$}
tmpFile=$filenamePrefix-tmp.txt
aws wafv2 list-rule-groups --scope CLOUDFRONT --region us-east-1 --query 'RuleGroups[].[Name, Id]' --output text > $tmpFile
while read name id; do
    aws wafv2 get-rule-group --scope CLOUDFRONT --region us-east-1 --name $name --id $id --output json > $filenamePrefix-rule-group-$name.json
    echo name="$name" id="$id"
done < $tmpFile
aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1 --query 'WebACLs[].[Name, Id]' --output text > $tmpFile
while read name id; do
    aws wafv2 get-web-acl --scope CLOUDFRONT --region us-east-1 --name $name --id $id --output json > $filenamePrefix-web-acl-$name.json
    echo name="$name" id="$id"
done < $tmpFile
aws wafv2 list-ip-sets --scope CLOUDFRONT --region us-east-1 --query 'IPSets[].[Name, Id]' --output text > $tmpFile
while read name id; do
    aws wafv2 get-ip-set --scope CLOUDFRONT --region us-east-1 --name $name --id $id --output json > $filenamePrefix-ip-set-$name.json
    echo name="$name" id="$id"
done < $tmpFile
