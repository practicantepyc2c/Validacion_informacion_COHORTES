from operator import index
from os import remove
from tokenize import String
from turtle import pos
import pandas as pd
import numpy as np
import os
from pathlib import Path
pd.options.display.max_rows = None
pd.options.display.max_columns = None
import openpyxl
import xlwings as xw
from datetime import datetime
parametrica_identificacion = "./Parametricas/tipos_identificacion.xlsx"
parametrica_codigos = "./Parametricas/codigos.xlsx"
parametrica_programa = "./Parametricas/Programas_Cohortes.xlsx"
from correo import envioCorreoError, envioCorreoCorrecto
import xlsxwriter
from shutil import copyfile

def validacionInfo(fichero,nombreArchivo):
	rutaArchivo = Path(fichero)
	print(rutaArchivo, "validacion")
	archivo = pd.read_excel(rutaArchivo, engine= "openpyxl")
	tipos_identificacion = pd.read_excel(parametrica_identificacion)
	codigosPermitidos = pd.read_excel(parametrica_codigos)
	programas_cohortes = pd.read_excel(parametrica_programa)
	
	# Creando archivo excel 📄
	archivoErrores = xlsxwriter.Workbook('Archivo-errores.xlsx', {'nan_inf_to_errors': True})
	hoja = archivoErrores.add_worksheet('Errores')
	hoja.write(0,0,"FILA")
	hoja.write(0,1,"DATO")
	hoja.write(0,2,"CODIGO ERROR")
	posicion = 0
	
	# Verificacion de campos vacios


	nulos = archivo.isnull()['Num_Doc']
	columnas_vacias_NumDoc = np.array(archivo[nulos].index.values)
	columnas_vacias_NumDoc = columnas_vacias_NumDoc + 2
	if (len(columnas_vacias_NumDoc) != 0):
		for i in range(len(columnas_vacias_NumDoc)):
			hoja.write(i+1, 0,columnas_vacias_NumDoc[i])
			hoja.write(i+1, 1,"")
			hoja.write(i+1, 2,"E1")
		posicion = posicion + len(columnas_vacias_NumDoc)
	

	nulos = archivo.isnull()['Tipo_Doc']
	columnas_vacias_TipoDoc = np.array(archivo[nulos].index.values)
	columnas_vacias_TipoDoc = columnas_vacias_TipoDoc + 2
	
	if (len(columnas_vacias_TipoDoc) != 0):
		for i in range(len(columnas_vacias_TipoDoc)):
			hoja.write(i+1+posicion,0,columnas_vacias_TipoDoc[i])
			hoja.write(i+1+posicion,1,"")
			hoja.write(i+1+posicion,2,"E2")
		posicion = posicion + len(columnas_vacias_TipoDoc)
	

	nulos = archivo.isnull()['Cod_CIE10']
	columnas_vacias_cod = np.array(archivo[nulos].index.values)
	columnas_vacias_cod = columnas_vacias_cod + 2
	if( len(columnas_vacias_cod) != 0):
		for i in range(len(columnas_vacias_cod)):
			hoja.write(i+1+posicion,0,columnas_vacias_cod[i])
			hoja.write(i+1+posicion,1,"")
			hoja.write(i+1+posicion,2,"E3")
		posicion = posicion + len(columnas_vacias_cod)
		

	nulos = archivo.isnull()['Programa']
	columnas_vacias_programa = np.array(archivo[nulos].index.values)
	columnas_vacias_programa = columnas_vacias_programa + 2 
	if (len(columnas_vacias_programa) != 0):
		for i in range(len(columnas_vacias_programa)):
			hoja.write(i+1+posicion,0,columnas_vacias_programa[i])
			hoja.write(i+1+posicion,1,"")
			hoja.write(i+1+posicion,2,"E5")
		posicion = posicion + len(columnas_vacias_programa)



	# CAMPOS CON VALORES INCORRECTOS
	# file.write('campos con valores incorrectos \n')
	#archivo.dropna(inplace=True)
	# Validar tipo de documento permitido
	archivo['Tipo_Doc'] = archivo['Tipo_Doc'].fillna('CC')
	tipo_docPermitido = archivo['Tipo_Doc'].isin(tipos_identificacion.tipo_identificacion)
	noPermitido = tipo_docPermitido.loc[tipo_docPermitido == False]
	columnas_incorrecto_tipo_doc = np.array(noPermitido.index.values)
	columnas_incorrecto_tipo_doc = columnas_incorrecto_tipo_doc + 2
	values_errores_tipo_doc = archivo['Tipo_Doc'][tipo_docPermitido == False].values
	if (len(columnas_incorrecto_tipo_doc) != 0):
		for i in range(len(columnas_incorrecto_tipo_doc)):
			hoja.write(i+1+posicion,0,columnas_incorrecto_tipo_doc[i])
			try:
				hoja.write(i+1+posicion,1,values_errores_tipo_doc[i])
			except:
				pass
			hoja.write(i+1+posicion,2,"A1")
		posicion = posicion + len(columnas_incorrecto_tipo_doc)
	

	# Validar numero de caracteres Cod_CIE10
	codigo = archivo['Cod_CIE10']
	archivo['Cod_CIE10'] = archivo['Cod_CIE10'].fillna('A000')
	Cod_CIE10Permitido = archivo['Cod_CIE10'].isin(codigosPermitidos.Codigos_permitidos)
	noPermitido = Cod_CIE10Permitido.loc[Cod_CIE10Permitido == False]
	columnas_incorrecto_Cod_CIE10 = noPermitido.index.values
	archivo['Cod_CIE10'][Cod_CIE10Permitido == False].values
	values_errores_Cod_CIE10 = np.array(archivo['Cod_CIE10'][Cod_CIE10Permitido == False].values)
	columnas_incorrecto_Cod_CIE10 = np.array(columnas_incorrecto_Cod_CIE10)
	columnas_incorrecto_Cod_CIE10 = columnas_incorrecto_Cod_CIE10 + 2		
	if (len(columnas_incorrecto_Cod_CIE10) != 0):
		for i in range(len(columnas_incorrecto_Cod_CIE10)):
			hoja.write(i+1+posicion,0,columnas_incorrecto_Cod_CIE10[i])
			try:
				hoja.write(i+1+posicion,1,values_errores_Cod_CIE10[i])
			except:
				pass
			hoja.write(i+1+posicion,2,"A2")
		posicion = posicion + len(columnas_incorrecto_Cod_CIE10)

	# Validacion seguimiento
	seguimiento = archivo['Seguimiento Programa']
	columnas_incorrecto_seguimiento = []
	values_errores_seguimiento = []
	seguimiento = seguimiento.fillna('Nulo')
	for i in range(len(seguimiento)):
		if seguimiento[i] != 'SI' and seguimiento[i] != 'NO' and seguimiento[i] != 'Nulo':
			columnas_incorrecto_seguimiento.append(i)
			values_errores_seguimiento.append(seguimiento[i])
	columnas_incorrecto_seguimiento = np.array(columnas_incorrecto_seguimiento)
	columnas_incorrecto_seguimiento = columnas_incorrecto_seguimiento + 2	
	if (len(columnas_incorrecto_seguimiento) != 0):
		for i in range(len(columnas_incorrecto_seguimiento)):
			hoja.write(i+1+posicion,0,columnas_incorrecto_seguimiento[i])
			try:
				hoja.write(i+1+posicion,1,values_errores_seguimiento[i])
			except:
				pass
			hoja.write(i+1+posicion,2,"B1")
		posicion = posicion + len(columnas_incorrecto_seguimiento)


	# Validar campos CONTROLADO, NO APLICA y NO CONTROLADO controlado NaN
	controlado = archivo['controlado']
	columnas_incorrecto_controlado = []
	values_errores_controlado = []
	controlado = controlado.fillna('Nulo')
	for i in range(len(controlado)):
		if controlado[i] != 'CONTROLADO' and controlado[i] != 'NO APLICA' and controlado[i] != 'NO CONTROLADO' and controlado[i] != 'Nulo':
			columnas_incorrecto_controlado.append(i)
			values_errores_controlado.append(controlado[i])
	columnas_incorrecto_controlado = np.array(columnas_incorrecto_controlado)
	columnas_incorrecto_controlado = columnas_incorrecto_controlado + 2
	if (len(columnas_incorrecto_controlado) != 0):
		for i in range(len(columnas_incorrecto_controlado)):
			hoja.write(i+1+posicion,0,columnas_incorrecto_controlado[i])
			try:
				hoja.write(i+1+posicion,1,values_errores_controlado[i])
			except:
				pass
			hoja.write(i+1+posicion,2,"B2")
		posicion = posicion + len(columnas_incorrecto_controlado)


	# Validar fecha > actual Fecha_Diagnostico
	fechas = archivo['Fecha_Diagnostico']
	columnas_incorrecto_fechas = []
	values_errores_fechas = []
	fechas = fechas.fillna('Nulo')
	for i in range(len(fechas)):
		try:
			if fechas[i] > datetime.now():
				values_errores_fechas.append(fechas[i])
				columnas_incorrecto_fechas.append(i)
		except:
			if fechas[i] != 'Nulo':
				values_errores_fechas.append(fechas[i])
				columnas_incorrecto_fechas.append(i)
	columnas_incorrecto_fechas = np.array(columnas_incorrecto_fechas)
	columnas_incorrecto_fechas = columnas_incorrecto_fechas + 2	
	if (len(columnas_incorrecto_fechas) != 0):
		for i in range(len(columnas_incorrecto_fechas)):
			hoja.write(i+1+posicion,0,columnas_incorrecto_fechas[i])
			try:
				hoja.write(i+1+posicion,1,values_errores_fechas[i])
			except:
				pass
			hoja.write(i+1+posicion,2,"B3")
		posicion = posicion + len(columnas_incorrecto_fechas)	

	archivo['Tipo_Doc'] = archivo['Tipo_Doc'].fillna('SALUD MENTAL')
	programa_permitido = archivo['Programa'].isin(programas_cohortes.PROGRAMAS)
	programa_nopermitido = programa_permitido.loc[programa_permitido == False]
	columnas_incorrecto_programa = np.array(programa_nopermitido.index.values)
	archivo['Programa'][programa_permitido == False].values
	columnas_incorrecto_programa = np.array(columnas_incorrecto_programa)
	columnas_incorrecto_programa = columnas_incorrecto_programa + 2
	values_errores_programa = np.array(archivo['Programa'][programa_permitido == False].values)
	print(values_errores_programa) 
	if (len(columnas_incorrecto_programa) != 0):
		for i in range(len(columnas_incorrecto_programa)):
			hoja.write(i+1+posicion,0,columnas_incorrecto_programa[i])
			try:
				hoja.write(i+1+posicion,1,values_errores_programa[i])
			except:
				pass
			hoja.write(i+1+posicion,2,"A2")
		posicion = posicion + len(columnas_incorrecto_programa)


	# Diccionario de errores 📕 ❌
	diccionario =  archivoErrores.add_worksheet('Diccionario de errores')
	diccionario.write(0,0,"CODIGO ERROR")
	diccionario.write(0,1,"DESCRIPCIÓN")
	diccionario.write(1,0,"E1")
	diccionario.write(1,1,"Campo NumDoc vacio")
	diccionario.write(2,0,"E2")
	diccionario.write(2,1,"Campo TipoDoc vacio")
	diccionario.write(3,0,"E3")
	diccionario.write(3,1,"Campo Cod_CIE10 vacio")
	diccionario.write(4,0,"E4")
	diccionario.write(4,1,"Campo fecha diagnostico vacio")
	diccionario.write(5,0,"E5")
	diccionario.write(5,1,"Campo programa vacio")
	diccionario.write(6,0,"A1")
	diccionario.write(6,1,"Tipo identificacion no existe en tabla referencia")
	diccionario.write(7,0,"A2")
	diccionario.write(7,1,"Tipo de codigo no permitido")
	diccionario.write(8,0,"B1")
	diccionario.write(8,1,"Valor de seguimiento no permitido los valores permitidos son: SI y NO")
	diccionario.write(9,0,"B2")
	diccionario.write(9,1,"Valor de controlado no permitido los valores permitidos son: CONTROLADO, NO APLICA y NO CONTROLADO")
	diccionario.write(10,0,"B3")
	diccionario.write(10,1,"El formato de fecha es el incorrecto")



	archivoErrores.close()

	# Enviar correo dependiendo si el archivo es correcto
	if(len(columnas_vacias_programa) == 0 and len(columnas_vacias_cod) == 0 and len(columnas_vacias_NumDoc) == 0 and len(columnas_vacias_TipoDoc) == 0 and len(columnas_incorrecto_Cod_CIE10) == 0 and len(columnas_incorrecto_controlado) == 0 and len(columnas_incorrecto_seguimiento) == 0 and len(columnas_incorrecto_tipo_doc) == 0 and len(columnas_incorrecto_fechas) == 0):
		destino = Path('Archivos_correctos',nombreArchivo)
		copyfile(fichero,destino)
		envioCorreoCorrecto(nombreArchivo)
	else:
		envioCorreoError(nombreArchivo)
	os.remove('Archivo-errores.xlsx')
	return print("archivo validado exitosamente")

#validacionInfo("Parametricas\programa-ARTRITIS-202207 - Claudia Yaneth Ramirez Murcia.xlsx","PROGRAMA-DIALISIS-202207 - Luisa Fernanda Sandoval Riaño.xlsx")
