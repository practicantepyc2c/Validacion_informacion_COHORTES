from pathlib import Path
from datetime import datetime
import os
filename = Path('C:/Users/practicante_pyc2_c/Documents/Code/Validacion_informacion_COHORTES/Prueba')

def cambiarNombre():
	listaDir = list(Path(filename).iterdir())
	for fichero in listaDir: 	
		fileName = fichero.name
		nuevonombre = fileName.replace("_","-")
		nuevoPath = Path(filename,nuevonombre)
		print(nuevoPath, "nuevoPath")
		print(fichero, "fichero normal")
		os.rename(fichero,nuevoPath)
	return listaDir