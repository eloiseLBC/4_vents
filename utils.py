from datetime import datetime, timedelta

import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
from constants import (TBNB_ID, BEARER_TOKEN, MESSAGE_TAKE_LINGE_FRIDAY, MESSAGE_PUT_LINGE_SUNDAY,
                       MESSAGE_PUT_TAKE_BEFORE_SATURDAY,
                       MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY,
                       MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_NEXT, MESSAGE_PUT_LAUNDRY, MESSAGE_PUT_TAKE_FRIDAY,
                       MESSAGE_TAKE_HOME_LAUNDRY, MESSAGE_TAKE_HOME_LAUNDRY_SUNDAY, MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_2,
                       MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY_SUNDAY, MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY)


# Récupérer le nom de la feuille Excel
def get_sheet_name(id_property):
    url = f"https://sandbox.turno.com/v2/properties/{id_property}"
    headers = {
        "Accept": "application/json",
        "TBNB-Partner-ID": TBNB_ID,
        "Authorization": BEARER_TOKEN
    }
    response = requests.get(url, headers=headers)
    # Vérifier le statut de la réponse
    if response.status_code == 200:
        sheet_name = response.json()["data"]["alias"]
        return sheet_name
    else:
        # Si la requête échoue, afficher un message d'erreur
        print("Erreur")
        return f"Erreur {response.status_code}: {response.text}"


# Récupérer les données d'une feuille Google Sheets
def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("Aux4Vents_DB")
    sheet = spreadsheet.worksheet(sheet_name)
    return sheet


# Request properties
def get_properties(id_property):
    url = f"https://sandbox.turno.com/v2/bookings/?properties[]={id_property}"
    headers = {
        "Accept": "application/json",
        "TBNB-Partner-ID": TBNB_ID,
        "Authorization": BEARER_TOKEN
    }
    return requests.get(url, headers=headers)


# Récupérer les dates de booking
def get_bookings_dates(id_property):
    response = get_properties(id_property)
    # Check response status
    if response.status_code == 200:
        total_bookings = response.json()["data"]["total"]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S')
        if total_bookings > 1:
            checkin = response.json()["data"]["items"][0]["checkin"]
            checkout = response.json()["data"]["items"][0]["checkout"]
            checkin_date = datetime.strptime(checkin, '%Y-%m-%dT%H:%M:%S.%fZ')
            checkout_date = datetime.strptime(checkout, '%Y-%m-%dT%H:%M:%S.%fZ')
            diff_now_checkin = checkin_date - now
            for item in response.json()["data"]["items"]:
                checkin_item = datetime.strptime(item["checkin"], '%Y-%m-%dT%H:%M:%S.%fZ')
                if (checkin_item - now) < diff_now_checkin:
                    checkin_date = checkin_item
                    checkout_date = datetime.strptime(item["checkout"], '%Y-%m-%dT%H:%M:%S.%fZ')
            print(f"Checkin date : {checkin_date}. Checkout date : {checkout_date}")
            return checkin_date, checkout_date
        elif total_bookings == 1:
            checkin = response.json()["data"]["items"][0]["checkin"]
            checkout = response.json()["data"]["items"][0]["checkout"]
            checkin_date = datetime.strptime(checkin, '%Y-%m-%dT%H:%M:%S.%fZ')
            checkout_date = datetime.strptime(checkout, '%Y-%m-%dT%H:%M:%S.%fZ')
            print(f"Checkin date : {checkin_date}. Checkout date : {checkout_date}")
            return checkin_date, checkout_date
        else:
            print("Aucune reservation")
            return 0, 0
    else:
        print("Erreur")
        return f"Erreur {response.status_code}: {response.text}"


# Get next booking checkin
def get_next_booking(id_property):
    response = get_properties(id_property)
    now = datetime.now()
    lst = []
    # Check response status
    if response.status_code == 200:
        for item in response.json()["data"]["items"]:
            lst.append(item["checkin"])
        dates = [datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ') for date_str in lst]
        closest_booking = min(dates, key=lambda date: abs(date - now))
        return closest_booking.date()
    else:
        print("Erreur")
        return f"Erreur {response.status_code}: {response.text}"


# Ecrire des données dans le google Sheet
def write_data_into_sheet(sheet, data):
    values_in_horodateur = sheet.col_values(1)
    nom_empty_values = [value for value in values_in_horodateur if value]
    row_to_write = len(nom_empty_values) + 1
    for i in range(3):
        sheet.update_cell(row_to_write, i + 1, data[i])


# Gestion des situations de notifications
def manage_bookings_notifications(checkin, checkout, linges_propres, id_property):
    # Get index day week of booking
    index_day_checkin = checkin.weekday() + 1
    index_day_checkout = checkout.weekday() + 1
    print(f"Day week checkin : {index_day_checkin}")
    print(f"Day week checkout : {index_day_checkout}")
    # Get next booking
    simplified_checkout = checkout.date()
    next_booking = get_next_booking(id_property)
    print(f"Simplified checkout : {simplified_checkout}")
    print(f"Simplified checkout type : {type(simplified_checkout)}")
    print(f"Next booking : {next_booking}")
    print(f"Next booking type : {type(next_booking)}")
    if linges_propres == 1:
        if index_day_checkin in (1, 2, 3, 4) and index_day_checkout == 5:
            # S2-1:4
            if next_booking == simplified_checkout:
                return MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY
            elif next_booking == (simplified_checkout + timedelta(days=1)):
                return MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_NEXT
            else:
                return MESSAGE_PUT_LAUNDRY
        elif index_day_checkin == 5 and index_day_checkout == 6:
            # S1 -5
            if next_booking == simplified_checkout:
                return MESSAGE_PUT_TAKE_BEFORE_SATURDAY
        elif index_day_checkin in (6, 7) and index_day_checkout == 6:
            # S1-6,7
            return MESSAGE_PUT_LINGE_SUNDAY
        elif index_day_checkin == 5 and index_day_checkout == 5:
            # S2-5
            return MESSAGE_PUT_TAKE_FRIDAY
        elif index_day_checkin == 6 and index_day_checkout == 5:
            # S2-6
            return MESSAGE_TAKE_HOME_LAUNDRY
        elif index_day_checkin == 7 and index_day_checkout == 5:
            # S2-7
            return MESSAGE_TAKE_HOME_LAUNDRY_SUNDAY
    elif linges_propres == 2:
        if index_day_checkin in (1, 2, 3, 4) and index_day_checkout == 5:
            # S3-1:4
            if next_booking == simplified_checkout:
                return MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY
            elif next_booking == (simplified_checkout + timedelta(days=1)):
                return MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_NEXT
            else:
                return MESSAGE_PUT_LAUNDRY
        elif index_day_checkin == 5 and index_day_checkout == 5:
            # S3-5
            return MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_2
        elif index_day_checkin == 6 and index_day_checkout == 5:
            # S3-6
            return MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY_SUNDAY
        elif index_day_checkin == 7 and index_day_checkout == 5:
            # S3-7
            return MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY
    else:
        # S1-1:4 & else
        return MESSAGE_TAKE_LINGE_FRIDAY


# Envoi de messages whatsapp
def send_whatsapp(number, name, message):
    # Votre Account SID de Twilio
    account_sid = 'ACf567f7cc362746309161d810eb1516a2'
    # Votre Auth Token de Twilio
    auth_token = '0694e59f667b7f0d4065f21a89d14103'
    client = Client(account_sid, auth_token)
    print(f"Name : {name}")
    print(f"Name : {message}")
    message = client.messages.create(
        to="whatsapp:+33" + str(number),
        from_="whatsapp:+14155238886",
        body="Rappel : " + name + message)
    print(message.sid)


# Trouver le numéro de téléphone d'un agent
def find_agent_number(data_turno):
    agent_name = data_turno['cleaner']['name']
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
