from twilio.rest import Client
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/turno-webhook', methods=['POST'])
def turno_webhook():
    data = request.json
    print("Données reçues:", data)
    # Implémentez votre logique ici
    process_data(data)
    return jsonify({"status": "success"}), 200


def process_data(data):
    # Implémentez votre logique de traitement des données ici
    print("Traitement des données:", data)
    # Par exemple, enregistrez les données dans une base de données ou effectuez une autre action


if __name__ == "__main__":
    app.run(port=5000)

#
# """ Envoi de messages whatsapp"""
# # Votre Account SID de Twilio
# account_sid = 'ACf567f7cc362746309161d810eb1516a2'
# # Votre Auth Token de Twilio
# auth_token = '0694e59f667b7f0d4065f21a89d14103'
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#     to="whatsapp:+33652750562",  # Remplacez par le numéro de téléphone du destinataire
#     from_="whatsapp:+14155238886",  # Remplacez par votre numéro Twilio
#     body="Vous êtes si belle mon amour, puis-je vous enlacer ? "
# )
# print(message.sid)
