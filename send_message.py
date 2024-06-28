from twilio.rest import Client
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Data received:", data)  # Logique de traitement ici
    return jsonify({"status": "success", "message": "Data processed successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

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
