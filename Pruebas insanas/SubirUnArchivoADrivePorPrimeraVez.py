from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Autenticación
gauth = GoogleAuth()
gauth.LoadClientConfigFile('C:\\Users\\Usuario\\Documents\\Programa de stock\\Pruebas insanas\\client_secret.json')
gauth.LocalWebserverAuth()  # Abre una ventana del navegador para autenticación

# Acceso al Google Drive
drive = GoogleDrive(gauth)

# Ruta del archivo CSV local que deseas subir
ruta_archivo_local = 'C:\\Users\\Usuario\\Documents\\Programa de stock\\DataBase.csv'

# Crear un archivo en Google Drive
archivo_drive = drive.CreateFile()
archivo_drive.SetContentFile(ruta_archivo_local)  # Establecer el contenido del archivo
archivo_drive.Upload()  # Subir el archivo

print("Archivo subido exitosamente a Google Drive.")