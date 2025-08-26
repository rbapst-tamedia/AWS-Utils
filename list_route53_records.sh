#!/bin/bash
for zone in `aws route53 list-hosted-zones --query 'HostedZones[*].Id' --output text`
do
	echo $zone
	records=`aws route53 list-resource-record-sets --hosted-zone-id $zone --output json`
	echo "$records" | jq -r '["Name", "Type", "Value"], (.ResourceRecordSets[] | [.Name, .Type, (.ResourceRecords | select(. != null) | map(.Value) | join(" ")), (.AliasTarget.DNSName? | select(. != null))]) | @csv' > ${zone:12}.csv
	echo "$records" > ${zone:12}.txt
done
