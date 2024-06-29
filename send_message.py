from datetime import datetime
from twilio.rest import Client
from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)


@app.route('/turno-webhook', methods=['POST', 'GET'])
def turno_webhook():
    if request.method == 'POST':
        data = request.json
        # Implémentez votre logique ici
        process_data(data)
        return jsonify({"status": "success"}), 200
    elif request.method == 'GET':
        return "Le serveur est en cours d'exécution et accepte les requêtes POST", 200
    else:
        return jsonify({"status": "method not allowed"}), 405


def process_data(data_turno):
    # TODO : Implémenter la logique de traitement des données ici
    # Données de l'API Turno
    print("Données reçues:", data_turno)

    # Récupérer les données sheets
    data_sheets = access_sheets(data_turno)
    horodateur_final = "2024-01-01 17:00:00"
    horodateur_final = datetime.strptime(horodateur_final, "%Y-%m-%d %H:%M:%S")
    for record in data_sheets:
        if record['Horodateur']:
            temp = datetime.strptime(record['Horodateur'], "%Y/%m/%d %H:%M:%S")
            if temp > horodateur_final:
                horodateur_final = temp
    # Checker sur la ligne de la dernière information
    print(f"Horodateur final : {horodateur_final}")


def send_whatsapp():
    """ Envoi de messages whatsapp"""
    # Votre Account SID de Twilio
    account_sid = 'ACf567f7cc362746309161d810eb1516a2'
    # Votre Auth Token de Twilio
    auth_token = '0694e59f667b7f0d4065f21a89d14103'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="whatsapp:+33652750562",  # Remplacez par le numéro de téléphone du destinataire
        from_="whatsapp:+14155238886",  # Remplacez par votre numéro Twilio
        body="Vous êtes si belle mon amour, puis-je vous enlacer ? "
    )
    print(message.sid)


def access_sheets(data):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
    # Autoriser le client gspread
    client = gspread.authorize(creds)
    spreadsheet = client.open("Aux4Vents_DB")
    sheet_name = data['data']['appartement']
    sheet = spreadsheet.worksheet(sheet_name)
    data_sheets = sheet.get_all_records()
    return data_sheets


if __name__ == "__main__":
    # Execution de Flask et traitement des données
    app.run(port=5000)
    # send_whatsapp();
    access_sheets()
