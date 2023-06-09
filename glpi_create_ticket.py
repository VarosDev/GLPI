import requests
import json
import sys

# --- Définition des variables globales --- #
glpi_url = "http://di.hdpmb.adm/apirest.php"    # URL de l'api GLPI sur le domaine.
app_token = "dCXTq9ZqLeOAemspvbE3P7SaHhVTV0mxLFLT4lzt"   # Token API de l'application. Récupéré via Configuration > Générale > API > Nom de l'API > Jeton d'application.
user = "Y2VudHJlb246NVdzNC05clQvOA=="   # Correspond à un couple {login}:{password} encodé en base64 pour accéder à son compte GLPI
liste_nouveaux_membres = sys.argv[1]   # Correspond à la liste des nouveaux utilisateur créé sur l'AD dans les dernières 120 secondes.


# --- Définition des différentes fonctions utilisées --- #
def init_session(url, token_app, user, liste):     # Fonction qui permet d'initialiser la connexion sur le GLPI.
    print("Début du programme initialisation de la session.")
    headers = {
        'Authorization': 'Basic ' + user,  # Correspond à un couple {login}:{password} encodé en base64 pour accéder à sont compte GLPI
        'App-Token': token_app
    }
    response = requests.post(url+"/initSession", headers=headers)   # Initialisation de la session GLPI avec les paramètres placé dans le header.
    if response.status_code == 200:     # Si response.status_code = 200 (OK) alors la session est bien initialisé on peut alors faire un ticket (fonction send_ticket)
        send_ticket(response.json()["session_token"], url, token_app, liste)  # Appel de la fonction send_ticket avec comme paramètre le token de session récupéré ainsi que la liste des nouveaux utilisateurs.
    else:
        print("Une erreur est survenue : " + str(response.status_code) + " - " + str(response.json()))  # Affiche un message d'erreur si la session n'a pas réussi a être initialisé

def send_ticket(token_session, url, token_app, liste):     # Fonction qui permet de créer et d'envoyer un ticket.
    print("Création du ticket.")
    headers = {
        "Content-Type": "application/json",
        "Session-Token": token_session,     # Correspond au token de session récupéré avec la fonction init_session
        'App-Token': token_app
    }
    ticket_data = {
        "input": {
            "type": "2",   # Correspond à l'ID de l'option du menu select (name: type) : Type du ticket > Demande.
            "itilcategories_id": "219",   # Correspond à l'ID de l'option du menu select (name: itilcategories_id) : Catégorie du ticket > Gestion de compte.
            "locations_id": "324",      # Correspond à l'ID de l'option du menu select (name: locations_id) : Lieu du ticket > Service Informatique.
            "name": "Création d'un nouvel utilisateur",     # Titre du ticket
            "content": "Un nouvel utilisateur vient d'être créé sur l'AD : " + liste   # Paramètre obligatoire dans GLPI. Contenu du ticket avec ainsi la liste des nouveaux utilisateurs.
        }
    }
    response = requests.post(url + "/Ticket", data=json.dumps(ticket_data), headers=headers)    # Envoi du ticket avec les paramètre placé dans le header et les données placé dans ticket_data.
    if response.status_code == 201:     # Si response.status_code = 201 (CREATED) alors le ticket a bien été créé on peut alors kill notre session avec killSession.
        print("Le ticket a bien été envoyé.")
        kill_session(token_session, url, token_app)  # Appel de la fonction kill_session.
    else:
        print("Une erreur est survenue : " + str(response.status_code) + " - " + str(response.json())) # Affiche un message d'erreur si ticket n'a pas réussi a être envoyé
        kill_session(token_session, url, token_app)  # Appel de la fonction kill_session.
    return(str(response.status_code) + " - " + str(response.json()))    # Retourne alors le code http de la réponse ainsi que l’état de la création du ticket

def kill_session(token_session, url, token_app):    # Fonction qui permet de kill la session en cours.
    headers = {
        "Content-Type": "application/json",
        "Session-Token": token_session,     # Correspond au token de session récupéré avec la fonction init_session
        'App-Token': token_app
    }
    response = requests.post(url + "/killSession", headers=headers)
    if response.status_code == 200 :    # Si response.status_code = 200 (OK) alors la session a bien été kill.
        print("Fin de la session.")
    else:
        print("Une erreur est survenue : " + str(response.status_code) + " - " + str(response.json())) # Affiche un message d'erreur si la session n'a pas réussi a être kill


# --- Script principal --- #
init_session(glpi_url, app_token, user, liste_nouveaux_membres)     # Appelle de la première fonction pour initialiser