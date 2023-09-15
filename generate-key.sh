#!/bin/bash

echo -n "Enter repo: "
read -r
echo "- $REPLY-$(openssl rand -hex 20)" >> keys.yaml