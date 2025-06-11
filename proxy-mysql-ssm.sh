#!/bin/bash
# Tunnel to RDS through aws ssm

AWS_SECRET=secret_with_connection_infos
DB_INFOS=$(aws secretsmanager get-secret-value --secret-id $AWS_SECRET --output text --query SecretString)
LAST_DEPLOYED=$(echo $DB_INFOS|jq -r '.lastDeployed')
DB_HOST=$(echo $DB_INFOS|jq -r .$LAST_DEPLOYED.Endpoint | cut -d: -f 1)
DB_PORT=$(echo $DB_INFOS|jq -r .$LAST_DEPLOYED.Endpoint | cut -d: -f 2)

INSTANCE_ID=$(echo get some instance id...)

LOCAL_PORT=$DB_PORT

aws ssm start-session --target $INSTANCE_ID --document-name AWS-StartPortForwardingSessionToRemoteHost --parameters '{"host": ["'$DB_HOST'"],"portNumber":["'$DB_PORT'"],"localPortNumber":["'$LOCAL_PORT'"]}'
