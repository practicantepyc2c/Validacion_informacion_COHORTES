from os import remove
from tokenize import String
import pandas as pd
import numpy as np
import os
from pathlib import Path
pd.options.display.max_rows = None
pd.options.display.max_columns = None
import openpyxl
from datetime import datetime
parametrica_identificacion = "./Parametricas/tipos_identificacion.xlsx"
from correo import envioCorreoError, envioCorreoCorrecto

def validacionInfo(fichero,nombreArchivo):

	rutaArchivo = Path(fichero)
	# rutaArchivo.replace("\\","/")
	print(rutaArchivo, "validacion")
	archivo = pd.read_excel(rutaArchivo)
	tipos_identificacion = pd.read_excel(parametrica_identificacion)

	nulos = archivo.isnull()['Num_Doc']
	columnas_vacias_NumDoc = np.array(archivo[nulos].index.values)
	columnas_vacias_NumDoc = columnas_vacias_NumDoc + 2

	nulos = archivo.isnull()['Tipo_Doc']
	columnas_vacias_TipoDoc = np.array(archivo[nulos].index.values)
	columnas_vacias_TipoDoc = columnas_vacias_TipoDoc + 2

	nulos = archivo.isnull()['Cod_CIE10']
	columnas_vacias_cod = np.array(archivo[nulos].index.values)
	columnas_vacias_cod = columnas_vacias_cod + 2

	nulos = archivo.isnull()['Fecha_Diagnostico']
	columnas_vacias_fechaDiagnostico = np.array(archivo[nulos].index.values)
	columnas_vacias_fechaDiagnostico = columnas_vacias_fechaDiagnostico + 2

	nulos = archivo.isnull()['Programa']
	columnas_vacias_programa = np.array(archivo[nulos].index.values)
	columnas_vacias_programa = columnas_vacias_programa + 2 

	nulos = archivo.isnull()['Periodo']
	columnas_vacias_periodo = np.array(archivo[nulos].index.values)
	columnas_vacias_periodo = columnas_vacias_periodo + 2

	nulos = archivo.isnull()['Seguimiento Programa']
	columnas_vacias_seguimiento = np.array(archivo[nulos].index.values)
	columnas_vacias_seguimiento = columnas_vacias_seguimiento + 2

	# CAMPOS CON VALORES INCORRECTOS

	# Validar tipo de documento permitido
	tipo_docPermitido = archivo['Tipo_Doc'].isin(tipos_identificacion.tipo_identificacion)
	noPermitido = tipo_docPermitido.loc[tipo_docPermitido == False]
	columnas_incorrecto_tipo_doc = np.array(noPermitido.index.values)
	columnas_incorrecto_tipo_doc = columnas_incorrecto_tipo_doc + 2

	# Validar numero de caracteres Cod_CIE10
	codigo = archivo['Cod_CIE10'].str.len() != 4
	columnas_incorrecto_codigo = np.array(archivo[codigo].index.values)
	columnas_incorrecto_codigo = columnas_incorrecto_codigo + 2

	seguimiento = (archivo['Seguimiento Programa'] != 'SI') & (archivo['Seguimiento Programa'] != 'NO')
	columnas_incorrecto_seguimiento = np.array(archivo[seguimiento].index.values)
	columnas_incorrecto_seguimiento = columnas_incorrecto_seguimiento + 2

	# Validar campos CONTROLADO, NO APLICA y NO CONTROLADO controlado NaN
	controlado = (archivo['controlado'] != 'CONTROLADO') & (archivo['controlado'] != 'NO APLICA') & (archivo['controlado'] != 'NO CONTROLADO')
	controlado = archivo[controlado]
	controlado = controlado.dropna()
	columnas_incorrecto_controlado = np.array(controlado.index.values)
	columnas_incorrecto_controlado = columnas_incorrecto_controlado + 2

	# Validar fecha > actual Fecha_Diagnostico
	# columnas_incorrecto_fecha = np.array([])
	# fecha = archivo['Fecha_Diagnostico'] > datetime.now()
	# fecha = archivo[fecha]
	# columnas_incorrecto_fecha = fecha.index.values


	# Archivo con errores 📋
	file = open("Errores.txt","w")
	file.write('campos vacios\n')
	file.write('Filas vacias en la columna NumDoc=%s '%columnas_vacias_NumDoc + '\n')
	file.write('Filas vacias en el TipoDoc=%s '%columnas_vacias_TipoDoc + '\n')
	file.write('Filas vacias en el Cod_CIE10=%s '%columnas_vacias_cod + '\n')
	file.write('Filas vacias en la fecha diagnostico=%s '%columnas_vacias_fechaDiagnostico + '\n')
	file.write('Filas vacias en la fecha programa=%s '%columnas_vacias_programa + '\n')
	file.write('campos con valores incorrectos \n')
	file.write('fila incorrecta en el tipo de documento=%s '%columnas_incorrecto_tipo_doc + '\n')
	file.write('fila incorrecta en el Cod_CIE10=%s '%columnas_incorrecto_codigo + '\n')
	file.write('fila incorrecta en el Seguimiento Programa=%s '%columnas_incorrecto_seguimiento + '\n')
	file.write('fila incorrecta en el controlado=%s '%columnas_incorrecto_controlado + '\n')
	# file.write('fila incorrecta en el fecha diagnostico=%s '%columnas_incorrecto_fecha)
	file.close()

	if(len(columnas_vacias_programa) == 0 and len(columnas_vacias_cod) == 0 and len(columnas_vacias_fechaDiagnostico) == 0 and len(columnas_vacias_periodo) == 0 and len(columnas_vacias_seguimiento) == 0 and len(columnas_vacias_NumDoc) == 0 and len(columnas_vacias_TipoDoc) == 0 and len(columnas_incorrecto_codigo) == 0 and len(columnas_incorrecto_controlado) == 0 and len(columnas_incorrecto_seguimiento) == 0 and len(columnas_incorrecto_tipo_doc) == 0):
		envioCorreoCorrecto(nombreArchivo)
	else:
		envioCorreoError(nombreArchivo)
	return print("archivo validado exitosamente")

# validacionInfo("programa_ERC-202207 - Wilmar Yidid Fracica Velasquez.xlsx")