from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

def auditorio_cohortes(fecha,remitente,asunto,nombre_Archivo):
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	KEY = 'key.json'
	SPREADSHEET_ID = '1nsxlNdyAzyndAvh1NWnt8JgMNtdxz0mp6qwaNeqMBDI'
	creds = None
	creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
	service = build('sheets', 'v4', credentials=creds)
	sheet = service.spreadsheets()

	# Debe ser una matriz por eso el doble [[]]
	values = [[fecha,remitente,asunto,nombre_Archivo]]
	# Llamamos a la api
	result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
								range='A1',
								valueInputOption='USER_ENTERED',
								body={'values':values}).execute()
	print(f"Datos insertados correctamente.\n{(result.get('updates').get('updatedCells'))}")
#auditorio_cohortes(datetime.now().strftime('%d/%m/%Y'),'camiloalex2000@gmail.com','Carga exitosa','archivo1')