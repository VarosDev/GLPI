import requests
import json
import sys

glpi_url = "http://YOUR-URL/apirest.php"
app_token = "YOU-APP-TOKEN"
user = "YOUR-BASE64-LOGIN:PASSWORD"

def init_session(url, token_app, user, liste):
    headers = {
        'Authorization': 'Basic ' + user,
        'App-Token': token_app
    }
    response = requests.post(url+"/initSession", headers=headers)
    if response.status_code == 200:
        send_ticket(response.json()["session_token"], url, token_app, liste)
    else:
        print("ERROR : " + str(response.status_code) + " - " + str(response.json()))

def send_ticket(token_session, url, token_app, liste):
    headers = {
        "Content-Type": "application/json",
        "Session-Token": token_session,
        'App-Token': token_app
    }
    ticket_data = {
        "input": {
            "type": "YOUR-TYPE-ID",
            "itilcategories_id": "YOUR-CATEGORIE-ID",
            "locations_id": "YOUR-LOCATION-ID",
            "name": "YOUR-TITLE",
            "content": "YOUR-CONTENT"
        }
    }
    response = requests.post(url + "/Ticket", data=json.dumps(ticket_data), headers=headers)
    if response.status_code == 201:
        print("SUCCESS")
        kill_session(token_session, url, token_app)
    else:
        print("ERROR : " + str(response.status_code) + " - " + str(response.json()))
        kill_session(token_session, url, token_app)
    return(str(response.status_code) + " - " + str(response.json()))

def kill_session(token_session, url, token_app):
    headers = {
        "Content-Type": "application/json",
        "Session-Token": token_session,
        'App-Token': token_app
    }
    response = requests.post(url + "/killSession", headers=headers)
    if response.status_code == 200 :
        print("Session has been killed")
    else:
        print("ERROR : " + str(response.status_code) + " - " + str(response.json()))



init_session(glpi_url, app_token, user, liste_nouveaux_membres)
