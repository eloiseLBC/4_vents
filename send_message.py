import time
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
from flask import Flask, request, jsonify
import gspread

from constants import MESSAGE_CHECK_FORM, MESSAGE_TAKE_LINGE

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


""" Mission assignée : Rappel d'aller chercher le linge """
def mission_assigned(data_turno):
    # Récupérer les données sheets
    sheet_name = data_turno['data']['appartement']
    sheet = get_sheet(sheet_name)
    data_sheets = sheet.get_all_records()
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
                send_whatsapp(agent_number, agent_name, MESSAGE_TAKE_LINGE)
            break


""" Ecrire des données dans le google Sheet """
def write_data_into_sheet(sheet, data):
    values_in_horodateur = sheet.col_values(1)
    nom_empty_values = [value for value in values_in_horodateur if value]
    row_to_write = len(nom_empty_values) + 1
    for i in range(3):
        sheet.update_cell(row_to_write, i + 1, data[i])


""" Pause du programme """
def time_break(time_to_sleep):
    print(f"Pause de {time_to_sleep} minutes : {datetime.now()}")
    time_second = time_to_sleep * 60
    time.sleep(time_second)
    print(f"Fin de la pause : {datetime.now()}")


""" Vérification du formulaire complété """
def check_form(appartment_name, horodateur):
    sheet = get_sheet(appartment_name)
    values_in_horodateur = sheet.col_values(1)
    last_horodateur = datetime.strptime("2024-01-01 00-00-00.000", "%Y-%m-%d %H-%M-%S.%f")
    for value in values_in_horodateur:
        last_horodateur = value
    if last_horodateur == "Horodateur":
        return False
    last_horodateur_obj = datetime.strptime(last_horodateur, "%d/%m/%Y %H:%M:%S")
    last_horodateur_formatted = last_horodateur_obj.strftime("%Y-%m-%d %H-%M-%S.%f")
    if last_horodateur_formatted < horodateur:
        return False
    return True


""" Mission commencée : Rappel de scanner le QR pour le formulaire """
def mission_started(data_turno):
    horodateur = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    service_agent = data_turno['data']['service_agent']
    appartment = data_turno['data']['appartement']
    data = [horodateur, service_agent, appartment]
    sheet = get_sheet("Mission commencée")
    # Ecrire les données dans le google Sheet
    write_data_into_sheet(sheet, data)
    time_break(10)
    # Vérifier si le formulaire a été soumis
    if not check_form(appartment, horodateur):
        agent_number, agent_name = find_agent_number(data_turno)
        send_whatsapp(agent_number, agent_name, MESSAGE_CHECK_FORM)


""" Récupération des données de l'API turno """
def process_data(data_turno):
    # TODO : Implémenter la logique de traitement des données ici
    # Données de l'API Turno
    print("Données Turno:", data_turno)
    if data_turno['event'] == "mission_assigned":
        mission_assigned(data_turno)
    elif data_turno['event'] == "mission_started":
        mission_started(data_turno)


""" Récupérer les données d'une feuille Google Sheets """
def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("Aux4Vents_DB")
    sheet = spreadsheet.worksheet(sheet_name)
    return sheet


""" Envoi de messages whatsapp"""
def send_whatsapp(number, name, message):
    # Votre Account SID de Twilio
    account_sid = 'ACf567f7cc362746309161d810eb1516a2'
    # Votre Auth Token de Twilio
    auth_token = '0694e59f667b7f0d4065f21a89d14103'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="whatsapp:+33" + str(number),
        from_="whatsapp:+14155238886",
        body="Rappel : " + name + message)
    print(message.sid)


""" Trouver le numéro de téléphone d'un agent """
def find_agent_number(data_turno):
    agent_name = data_turno['data']['service_agent']
    print(f"Nom de l'agent : {agent_name}")
    # Récupérer les données des agents
    sheet = get_sheet("Agents")
    agents_data = sheet.get_all_records()
    print(f"Données de l'agent  : {agents_data}")
    for agent in agents_data:
        name = agent["Nom de l'agent"]
        phone_number = agent["Téléphone"]
        if name == agent_name:
            return phone_number, name


if __name__ == "__main__":
    # Execution de Flask et traitement des données
    app.run(port=5000)
