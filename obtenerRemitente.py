from unittest import result
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import numpy as np
import os
import pickle
import time

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1xlBiWPL_QVa5L6qclFU-Me9OgeFTqegr9mXNoI1MNd8'
SAMPLE_RANGE_NAME = 'A1:AA1000'

def ultimoCorreo(archivo):
	# Abriendo spreadsheet
	print("Obteniendo correo del archivo",archivo)
	time.sleep(30)
	global values_input, service
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'my_json_file.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	
	service = build('sheets', 'v4', credentials=creds)

	sheet = service.spreadsheets()
	result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,range=SAMPLE_RANGE_NAME).execute()
	values_input = result_input.get('values', [])

	
	if not values_input and not values_expansion:
		print('No data found.')

	# Lectura dea archivo
	df=pd.DataFrame(values_input[1:], columns=values_input[0])
	correos = df['Correo'] 
	# wilmar = df['Correo'] == 'reportesprestadoresaps@colsanitas.com'
	# Obtener correo de archivo
	archivo_recibidos = df['Programa'] == archivo
	archivos_recibidos = np.array(df[archivo_recibidos].index.values)
	try:
		print(archivos_recibidos[-1])
	except:
		ultimoCorreo(archivo)
	ubicacionCorreo = archivos_recibidos[-1]
	print(ubicacionCorreo,"Ubicacion")
	print("Programa recibido",archivo)
	print(correos[ubicacionCorreo],"correo apuntador")
	# print(df[wilmar])
	return correos[ubicacionCorreo]
#ultimoCorreo('programa_HTA-202208 - Laura Maria Zabala Sierra.xlsx')