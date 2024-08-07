import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

""" Récupérer les données d'une feuille Google Sheets """
def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("Aux4Vents_DB")
    sheet = spreadsheet.worksheet(sheet_name)
    return sheet


""" Ecrire des données dans le google Sheet """
def write_data_into_sheet(sheet, data):
    values_in_horodateur = sheet.col_values(1)
    nom_empty_values = [value for value in values_in_horodateur if value]
    row_to_write = len(nom_empty_values) + 1
    for i in range(3):
        sheet.update_cell(row_to_write, i + 1, data[i])


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