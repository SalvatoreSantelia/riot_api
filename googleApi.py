from googleapiclient.discovery import build
from settaggi import *
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

sheets = build('sheets', 'v4', credentials=creds)
drive = build('drive', 'v3', credentials=creds)


def creaFoglio(title, carica=True):
    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    foglio = sheets.spreadsheets().create(body=spreadsheet,
                                          fields='spreadsheetId')
    foglio = foglio.execute()
    if carica: caricaFoglioSuDrive(foglio.get("spreadsheetId"))
    return foglio


def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))


def caricaFoglioSuDrive(id):
    batch = drive.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': EMAIL,
        'sendNotificationEmails': False
    }
    batch.add(drive.permissions().create(
        fileId=id,
        body=user_permission,
        fields='id',
    ))
    batch.execute()


def apriFoglio(nome):
    return drive.files().get(fileId=getIdFoglioFromName(nome)).execute()


def appendiRigheFoglio(name, righe, inputType="USER_ENTERED", my_range="Sheet1!A1"):
    id = getIdFoglioFromName(name)
    return sheets.spreadsheets().values().append(spreadsheetId=id,
                                                 range=my_range, valueInputOption=inputType,
                                                 body={"values": righe}).execute()


def clonaFoglio(nome_originale, nome_clonato=""):
    if nome_clonato == "": nome_clonato = nome_originale + AGGIUNTA_NOME_CLONATO
    id_originale = getIdFoglioFromName(nome_originale)
    foglio_copiato = drive.files().copy(fileId=id_originale).execute()
    body = {"name": nome_clonato}
    drive.files().update(fileId=foglio_copiato["id"], body=body).execute()
    caricaFoglioSuDrive(foglio_copiato["id"])
    return foglio_copiato


def getIdFoglioFromName(name):
    return drive.files().list(fields='files(id, name)',
                              q="name = '{0}'".format(name)).execute()["files"][0]["id"]
