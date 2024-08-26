#!/bin/bash

# Définir les fichiers de log
FLASK_LOG="flask.log"
LOCAL_TUNNEL_LOG="localtunnel.log"

# Démarrer le serveur Flask en arrière-plan
echo "Démarrage du serveur Flask..."
nohup python3 send_message.py > $FLASK_LOG 2>&1 &

sleep 10

# Démarrer LocalTunnel en arrière-plan
echo "Démarrage de LocalTunnel..."
nohup  ngrok http --domain=nominally-logical-pegasus.ngrok-free.app 80 > $LOCAL_TUNNEL_LOG 2>&1 &

echo "Le serveur Flask et LocalTunnel sont en cours d'exécution."
