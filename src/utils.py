from datetime import datetime, timedelta
import gspread
import requests
from src.send_message import logger
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
from src.constants import (MESSAGE_TAKE_LINGE_FRIDAY, MESSAGE_PUT_LINGE_SUNDAY,
                       MESSAGE_PUT_TAKE_BEFORE_SATURDAY,
                       MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY,
                       MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_NEXT, MESSAGE_PUT_LAUNDRY, MESSAGE_PUT_TAKE_FRIDAY,
                       MESSAGE_TAKE_HOME_LAUNDRY, MESSAGE_TAKE_HOME_LAUNDRY_SUNDAY, MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_2,
                       MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY_SUNDAY, MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY)
from secrets_variables import TBNB_ID, BEARER_TOKEN, ACCOUNT_SID


# Get sheet name
def get_sheet_name(id_property):
    url = f"https://api.turno.com/v2/properties/{id_property}"
    headers = {
        "Accept": "application/json",
        "TBNB-Partner-ID": TBNB_ID,
        "Authorization": BEARER_TOKEN
    }
    response = requests.get(url, headers=headers)
    # Check request statu
    if response.status_code == 200:
        sheet_name = response.json()["data"]["alias"]
        logger.info(f"Sheet name : {sheet_name}")
        return sheet_name
    else:
        # If request failed : print error message
        logger.info("Error")
        return f"Error {response.status_code}: {response.text}"


# Get sheet data
def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('../secrets/credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("../secrets/Aux4Vents_DB")
    sheet = spreadsheet.worksheet(sheet_name)
    return sheet


# Request properties
def get_properties(id_property):
    url = f"https://api.turno.com/v2/bookings/?properties[]={id_property}"
    headers = {
        "Accept": "application/json",
        "TBNB-Partner-ID": TBNB_ID,
        "Authorization": BEARER_TOKEN
    }
    return requests.get(url, headers=headers)


def get_name_surname_cleaner(agent_id):
    url = f"https://api.turno.com/v2/contractors/"
    headers = {
        "Accept": "application/json",
        "TBNB-Partner-ID": TBNB_ID,
        "Authorization": BEARER_TOKEN
    }
    response = requests.get(url, headers=headers)
    # Check request statu
    if response.status_code == 200:
        items = response.json()["data"]["items"]
        for item in items:
            if item["id"] == agent_id:
                first_name = item["first_name"]
                last_name = item["last_name"]
                long_name = f"{first_name} {last_name}"
                return long_name
    else:
        # If request failed : print error message
        logger.info("Error")
        return f"Error {response.status_code}: {response.text}"


# Get booking dates
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
            logger.info(f"Checkin date : {checkin_date}. Checkout date : {checkout_date}")
            return checkin_date, checkout_date
        elif total_bookings == 1:
            checkin = response.json()["data"]["items"][0]["checkin"]
            checkout = response.json()["data"]["items"][0]["checkout"]
            checkin_date = datetime.strptime(checkin, '%Y-%m-%dT%H:%M:%S.%fZ')
            checkout_date = datetime.strptime(checkout, '%Y-%m-%dT%H:%M:%S.%fZ')
            logger.info(f"Checkin date : {checkin_date}. Checkout date : {checkout_date}")
            return checkin_date, checkout_date
        else:
            logger.info("No reservation")
            return 0, 0
    else:
        logger.info("Error")
        return f"Error {response.status_code}: {response.text}"


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
        logger.info("Error")
        return f"Error {response.status_code}: {response.text}"


def concat_name(data_turno):
    agent_lastname = data_turno["data"]["assignment"]["contractor"]["last_name"]
    agent_surname = data_turno["data"]["assignment"]["contractor"]["first_name"]
    return f"{agent_surname} {agent_lastname}"


# Write data into Google Sheets
def write_data_into_sheet(sheet, data):
    values_in_horodateur = sheet.col_values(1)
    nom_empty_values = [value for value in values_in_horodateur if value]
    row_to_write = len(nom_empty_values) + 1
    for i in range(3):
        sheet.update_cell(row_to_write, i + 1, data[i])


# Managing notification event
def manage_bookings_notifications(checkin, checkout, linges_propres, id_property):
    # Get index day week of booking
    index_day_checkin = checkin.weekday() + 1
    index_day_checkout = checkout.weekday() + 1
    logger.info(f"Day week checkin : {index_day_checkin}")
    logger.info(f"Day week checkout : {index_day_checkout}")
    # Get next booking
    simplified_checkout = checkout.date()
    next_booking = get_next_booking(id_property)
    logger.info(f"Simplified checkout : {simplified_checkout}")
    logger.info(f"Simplified checkout type : {type(simplified_checkout)}")
    logger.info(f"Next booking : {next_booking}")
    logger.info(f"Next booking type : {type(next_booking)}")
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
        else:
            return MESSAGE_TAKE_LINGE_FRIDAY
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
            return MESSAGE_TAKE_LINGE_FRIDAY
    else:
        # S1-1:4 & else
        return MESSAGE_TAKE_LINGE_FRIDAY


# Send WhatsApp message
def send_whatsapp(number, name, message):
    # Votre Account SID de Twilio
    account_sid = ACCOUNT_SID
    # Votre Auth Token de Twilio
    auth_token = '0694e59f667b7f0d4065f21a89d14103'
    client = Client(account_sid, auth_token)
    logger.info(f"Name : {name}")
    logger.info(f"Message : {message}")
    message = client.messages.create(
        to="whatsapp:+33" + str(number),
        from_="whatsapp:+14155238886",
        body="Rappel : " + str(name) + str(message))
    logger.info(message.sid)


# Find cleaner number
def find_agent_number(data_turno):
    agent_id = data_turno['data']['assignment']['contractor']['id']
    # Récupérer le nom et le prénom de l'agent d'entretien
    agent_name = get_name_surname_cleaner(agent_id)
    logger.info(f"Nom de l'agent : {agent_name}")
    # Récupérer les données des agents
    sheet = get_sheet("Agents")
    agents_data = sheet.get_all_records()
    logger.info(f"Données de l'agent  : {agents_data}")
    for agent in agents_data:
        name = agent["Nom de l'agent"]
        phone_number = agent["Téléphone"]
        if name == agent_name:
            return phone_number, name
