#!/bin/bash

echo "Enter repo: "
read -r
echo "- $REPLY-$(openssl rand -hex 20)" >> keys.yaml