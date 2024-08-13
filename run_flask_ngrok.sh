#!/bin/bash

while true; do
    # Start ngrok and save its output (the public URL)
    C:\Users\elois\Downloads\ngrok-v3-stable-windows-amd64\ngrok http --domain=daring-peacock-strong.ngrok-free.app 80 > ngrok.log &

    # Wait for ngrok to initialize and write its URL
    sleep 5

    # Extract the public URL from ngrok's output
    URL=$(grep -o 'https://[a-z0-9]*\.ngrok\.io' ngrok.log | head -n 1)

    echo "Public URL: $URL"

    # Start your Flask app
    python app.py

    # Restart everything if the Flask app stops
    echo "Flask app has stopped. Restarting ngrok and Flask..."
    killall ngrok
done
