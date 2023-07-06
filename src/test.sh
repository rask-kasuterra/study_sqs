#!/bin/bash

age=$(aws sqs get-queue-attributes --queue-url https://sqs.ap-northeast-1.amazonaws.com/610342850487/test_queue --attribute-names OldestMessageAge | jq -r ".Attributes.OldestMessageAge")
#echo "age: ${age}"

min=$((age/1000/60))
sec=$((age/1000%60))
echo "${min}:${sec}"
