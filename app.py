from distutils.debug import DEBUG
from importlib.resources import path
from mimetypes import init
import time
import os
from pathlib import Path
from validacion import validacionInfo
from cambiarNombre import cambiarNombre
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import win32console
import win32gui
from os import remove
path = Path('Prueba')

class MyEventHandler(FileSystemEventHandler):
	def on_created(self,event):
		print("archivo creado")
		self.wait_file_created(event.src_path)
		with os.scandir(path) as ficheros:
			for fichero in ficheros:
				fileName = fichero.name
				validacionInfo(fichero,fileName)
				with open(fichero, newline='', encoding="utf8") as File:
					File.close()
					remove(File.name)
				
	def on_deleted(self,event):
		print(event.src_path,"borrado")

	def wait_file_created(self, source_path):
		historicalSize = -1
		while(historicalSize != os.path.getsize(source_path)):
			historicalSize = os.path.getsize(source_path)
			time.sleep(1)

	def on_moved(self,event):
		print("archivo movido")
	

 
def Observador():
	ventana = win32console.GetConsoleWindow()
	win32gui.ShowWindow(ventana, 0)
	print("Proceso terminado")


	
	observer = Observer()
	observer.schedule(MyEventHandler(), path , recursive=True)
	observer.start()
	try:
		print("Monitoreando")
		while observer.is_alive():
			observer.join(1)
	except KeyboardInterrupt:
			observer.stop()
			print("Terminado")
	observer.join()
Observador()