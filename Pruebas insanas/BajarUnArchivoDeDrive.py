from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
# Intentar cargar las credenciales desde el archivo creds.json
gauth = GoogleAuth()
gauth.LoadCredentialsFile("creds.json")

if gauth.credentials is None:
    # Si no hay credenciales almacenadas, realiza el proceso de autenticación y autorización
    gauth.LoadClientConfigFile('C:\\Users\\Usuario\\Documents\\Programa de stock\\Pruebas insanas\\client_secret.json')
    gauth.LocalWebserverAuth()

    # Guarda las credenciales en un archivo (creds.json) para su uso posterior
    gauth.SaveCredentialsFile("creds.json")
elif gauth.access_token_expired:
    # Si las credenciales están presentes pero expiraron, refresca el token
    gauth.Refresh()
else:
    # Las credenciales existen y no han expirado
    pass

# Resto del código para acceder y trabajar con Google Drive usando gauth...
from pydrive.drive import GoogleDrive
import os

# Acceso al Google Drive
drive = GoogleDrive(gauth)

file_id = '1dt8Q7mLxJg8ihAXykiAwAiRQresD9uym'

# Crear un archivo en Google Drive
archivo_drive = drive.CreateFile({'id': file_id})
archivo_drive.GetContentFile('DataBase.csv')

print("Archivo bajado exitosamente de Google Drive.")