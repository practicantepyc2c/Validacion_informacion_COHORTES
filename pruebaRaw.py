from pathlib import Path
from datetime import datetime

filename = Path('Prueba')
prueba = Path('G:\\Mi unidad\\Recepción Programas EPS (File responses)\\Adjuntar archivo de cohortes (File responses)\\Archivos validos\\programa_HEPATITIS_C-202207 - Andrea Carolina Castro Tobon.xlsx')
print(prueba)
prueba.replace("\\","/")


# listaDir = list(Path(filename).iterdir())
# for fichero in listaDir:
# 	print(fichero)