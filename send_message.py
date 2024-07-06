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
    print("Données Turno:", data_turno)

    # Récupérer les données sheets
    sheet_name = data_turno['data']['appartement']
    data_sheets = access_sheets(sheet_name)
    print(f"Données google sheets {data_sheets}")
    horodateur_final = "01/01/2024 17:00:00"
    horodateur_final = datetime.strptime(horodateur_final, "%d/%m/%Y %H:%M:%S")
    for record in data_sheets:
        if record['Horodateur']:
            temp = datetime.strptime(record['Horodateur'], "%d/%m/%Y %H:%M:%S")
            if temp > horodateur_final:
                horodateur_final = temp

    for row in data_sheets:
        horodateur_row = datetime.strptime(row['Horodateur'], "%d/%m/%Y %H:%M:%S")
        if horodateur_row == horodateur_final:
            linges_propres = row['Nombre de linges propres restants']
            print(f"Valeur de linges propres restants : {linges_propres}")
            if linges_propres == 1:
                agent_number, agent_name = find_agent_number(data_turno)
                send_whatsapp(agent_number, agent_name)
            break


def send_whatsapp(number, name):
    """ Envoi de messages whatsapp"""
    # Votre Account SID de Twilio
    account_sid = 'ACf567f7cc362746309161d810eb1516a2'
    # Votre Auth Token de Twilio
    auth_token = '0694e59f667b7f0d4065f21a89d14103'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="whatsapp:+33" + str(number),
        from_="whatsapp:+14155238886",
        body="Rappel : " + name + ", vous devez aller chercher le linge propre à la laverie partenaire WashBar au : 39 "
                                  "Rue Ausone, 33000, Bordeaux. Attention : Le WashBar est fermé le samedi, ainsi que "
                                  "le dimanche jusqu'à 15h."
    )
    print(message.sid)


def find_agent_number(data_turno):
    agent_name = data_turno['data']['service_agent']
    print(f"Nom de l'agent : {agent_name}")
    # Récupérer les données des agents
    agents_data = access_sheets("Agents")
    print(f"Données de l'agent  : {agents_data}")
    for agent in agents_data:
        name = agent["Nom de l'agent"]
        phone_number = agent["Téléphone"]
        if name == agent_name:
            return phone_number, name


def access_sheets(sheet_name):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
    # Autoriser le client gspread
    client = gspread.authorize(creds)
    spreadsheet = client.open("Aux4Vents_DB")
    sheet = spreadsheet.worksheet(sheet_name)
    data_sheets = sheet.get_all_records()
    return data_sheets


if __name__ == "__main__":
    # Execution de Flask et traitement des données
    app.run(port=5000)
