#!/bin/bash

publicIp=$(curl -# checkip.amazonaws.com)

echo 'Server Public IP: '$publicIp

export AWS_ACCESS_KEY_ID=....................
export AWS_SECRET_ACCESS_KEY=...........................................

cat <<EOT > zone.json
{
    "Comment": "Update record to reflect new IP address of home router",
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "jenkins.xcoder.pp.ua.",
                "Type": "A",
                "TTL": 300,
                "ResourceRecords": [
                    {
                        "Value": "$publicIp"
                    }
                ]
            }
        }
    ]
}
EOT

aws route53 change-resource-record-sets --hosted-zone-id Z0118956EU069IAZHTCP --change-batch file://zone.json > /dev/null

rm zone.json

unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY

echo 'Public IP added to route53 hosted zone '



