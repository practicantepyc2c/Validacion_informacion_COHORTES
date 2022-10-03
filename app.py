from distutils.debug import DEBUG
import time
import os
from pathlib import Path
from validacion import validacionInfo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_created(event):
	print("archivo creado")
	listaDir = list(Path(path).iterdir())
	for fichero in listaDir:
		print(fichero, "app")
		validacionInfo(fichero,fichero.name)
		with open(fichero) as File:
			File.close()
			fichero.unlink()

def on_deleted(event):
	print("archivo borrado")


def on_moved(event):
	print("archivo movido")

 
if __name__ == "__main__":

	event_handler = FileSystemEventHandler()
	# llamando funciones
	event_handler.on_created = on_created
	event_handler.on_deleted = on_deleted
	event_handler.on_moved = on_moved

	path = Path('G:/Mi unidad/Recepción Programas EPS (File responses)/Adjuntar archivo de cohortes (File responses)/Archivos validos')
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()
	try:
		print("Monitoreando")
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
		print("Terminado")
	observer.join()