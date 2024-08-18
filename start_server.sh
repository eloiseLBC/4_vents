#!/bin/bash

# Démarrer le serveur Flask en arrière-plan
echo "Démarrage du serveur Flask..."
nohup python3 send_message.py &

sleep 10

# Démarrer LocalTunnel en arrière-plan
echo "Démarrage de LocalTunnel..."
nohup lt --port 3000 &

echo "Le serveur Flask et LocalTunnel sont en cours d'exécution."
