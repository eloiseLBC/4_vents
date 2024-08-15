#!/bin/bash
git add .
git commit -m "Deploy test"
git pull origin main
sudo systemctl restart gunicorn
