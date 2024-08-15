#!/bin/bash
# shellcheck disable=SC2164
cd /home/ec2-user/4vents
git pull origin main
sudo systemctl restart send_message.py
