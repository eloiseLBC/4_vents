import logging
import sys
import time
from datetime import datetime
from flask import Flask, request, jsonify
import src.utils as utils
import requests
from secrets_variables import BEARER_TOKEN, TBNB_ID
from src.constants import MESSAGE_CHECK_FORM

app = Flask(__name__)
# Logger configuration
logging.basicConfig(filename='flask.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def mission_assigned_treatment(data_turno):
    id_property = data_turno['data']['booking ']['property_id']
    # Récupérer les données sheets
    logger.info(id_property)
    sheet_name = utils.get_sheet_name(id_property)
    sheet = utils.get_sheet(sheet_name)
    data_sheets = sheet.get_all_records()
    logger.info(f"Données google sheets {data_sheets}")
    horodateur_final = "01/01/2024 17:00:00"
    horodateur_final = datetime.strptime(horodateur_final, "%d/%m/%Y %H:%M:%S")
    for record in data_sheets:
        if record['Horodateur']:
            temp = datetime.strptime(record['Horodateur'], "%d/%m/%Y %H:%M:%S")
            if temp > horodateur_final:
                horodateur_final = temp

    # Récupérer nombre de linges propres restants
    for row in data_sheets:
        horodateur_row = datetime.strptime(row['Horodateur'], "%d/%m/%Y %H:%M:%S")
        if horodateur_row == horodateur_final:
            linges_propres = row['Nombre de linges propres restants']
            logger.info(f"Valeur de linges propres restants : {linges_propres}")
            if linges_propres in (1, 2):
                # Checker les dates de bookings
                checkin, checkout = utils.get_bookings_dates(id_property)
                message_to_send = utils.manage_bookings_notifications(checkin, checkout, linges_propres, id_property)
                logger.info(f"Message to send : {str(message_to_send)}")
                """ Si l'envoi de message se fait à l'agent d'entretien et non plus uniquement à Joan Busque,
                Merci de décommenter la ligne suivante et de remplacer : 
                utils.send_whatsapp("0652750562", "Joan Busque", message_to_send)
                par : 
                utils.send_whatsapp(agent_number, agent_name, message_to_send)"""
                # agent_number, agent_name = utils.find_agent_number(data_turno)
                # Renseigner le numéro de téléphone de Joan
                utils.send_whatsapp("652750562", "Joan Busque", message_to_send)
            break


def time_break(time_to_sleep):
    logger.info(f"Pause de {time_to_sleep} minutes : {datetime.now()}")
    time_second = time_to_sleep * 60
    time.sleep(time_second)
    logger.info(f"Fin de la pause : {datetime.now()}")


def check_form(appartment_name, horodateur):
    sheet = utils.get_sheet(appartment_name)
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


def mission_started_treatment(data_turno):
    horodateur = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    service_agent = utils.concat_name(data_turno)
    logger.info(f"Agent name : {service_agent}")
    appartment = data_turno['data']['property_alias']
    data = [horodateur, service_agent, appartment]
    sheet = utils.get_sheet("Mission commencée")
    # Ecrire les données dans le google Sheet
    utils.write_data_into_sheet(sheet, data)
    time_break(1)
    # Vérifier si le formulaire a été soumis
    if not check_form(appartment, horodateur):
        agent_number, agent_name = utils.find_agent_number(data_turno)
        utils.send_whatsapp(agent_number, agent_name, MESSAGE_CHECK_FORM)


@app.route('/')
def home():
    return "Page Home du serveur Flask"


# Mission assignée : Envoi message Whatsapp si le linge doit être récupéré
@app.route('/webhook_assigned', methods=['POST', 'GET'])
def mission_assigned():
    if request.method == 'POST':
        data_turno = request.json
        logger.info(data_turno)
        """ Mission assignée : Rappel d'aller chercher le linge, Rappel de déposer le linge """
        mission_assigned_treatment(data_turno)
        return jsonify({"status": "success"}), 200
    elif request.method == 'GET':
        return "Le serveur est en cours d'exécution et accepte les requêtes POST", 200
    else:
        return jsonify({"status": "method not allowed"}), 405


# Mission commencée : Rappel pour remplir le formulaire
@app.route('/webhook_started', methods=['POST', 'GET'])
def mission_started():
    if request.method == 'POST':
        data_turno = request.json
        logger.info(data_turno)
        """ Mission assignée : Rappel d'aller chercher le linge, Rappel de déposer le linge """
        mission_started_treatment(data_turno)
        return jsonify({"status": "success"}), 200
    elif request.method == 'GET':
        return "Le serveur est en cours d'exécution et accepte les requêtes POST", 200
    else:
        return jsonify({"status": "method not allowed"}), 405


# GET list of proprieties / POST create propriety
@app.route('/v2/properties', methods=['POST', 'GET'])
def create_properties():
    url = "https://api.turno.com/v2/properties/"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "TBNB-Partner-ID": TBNB_ID,
    }
    if request.method == 'POST':
        return jsonify({"status": "success"}), 200
    elif request.method == 'GET':
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            sys.exit(1)
    else:
        return jsonify({"status": "method not allowed"}), 405


# GET list of proprieties / POST create propriety
@app.route('/v2/bookings/', methods=['POST', 'GET'])
def get_bookings():
    url = "https://api.turno.com/v2/bookings/"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "TBNB-Partner-ID": TBNB_ID,
    }
    if request.method == 'POST':
        return jsonify({"status": "success"}), 200
    elif request.method == 'GET':
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            sys.exit(1)
    else:
        return jsonify({"status": "method not allowed"}), 405


@app.errorhandler(404)
def not_found(error):
    return jsonify("Resource not found"), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify("Internal server error"), 500


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Error : {e}")
