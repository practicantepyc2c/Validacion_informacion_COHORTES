from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from os import remove

class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(event.src_path, "modificado.")
 
    
    def on_created(self, event):
        archivo_entrante = None
        reporte = ""
        try:
            directorio = "Solicitud"
            
            with os.scandir(directorio) as ficheros:
                for fichero in ficheros:
                    print('Solitud')
                    archivo_entrante = fichero
                    if(fichero.name.split("=")[0] == "ReportePorDI"):
                        reporte = "usuarios"   
                        filtrar = FiltrarUsuarios()
                        filtrar.inicio(fichero)
                        with open(fichero, newline='', encoding="utf8") as File:
                            File.close()
                            remove(File.name)
                    else:    
                        with open(fichero, newline='' , encoding="utf8") as File:
                            archivo_entrante = fichero
                            reporte = "departamento"
                            reader = csv.reader(File,delimiter=':')
                            datos = []
                            for row in reader:
                                if(row != None):
                                    datos.append(row[0])
                            filtrar = None
                            print("Recibo de primeras lo siguiente:")
                            print(datos[0], "   ", datos[1])
                            if(datos[1] == "BusquedaDepartamento"):
                                filtrar = FiltrarDepartamento()
                                filtrar.inicio(datos, File.name)
                            File.close()
                            remove(File.name)
            print("Archivo Creado Satisfactoriamente")
        except Exception as e:
            print("Error...")
            print(e)
            if (str(e) != "line contains NUL"):
                error_generado = ErrorArchivo()
                error_generado.inicio(archivo_entrante, e, reporte)
    
    def on_moved(self, event):
        print(event.src_path, "movido a", event.dest_path)
    
    def on_deleted(self, event):
        print(event.src_path, "eliminado.")
    

ventana = win32console.GetConsoleWindow()
win32gui.ShowWindow(ventana, 0)
print("Proceso terminado")


observer = Observer()
observer.schedule(MyEventHandler(), "Solicitud", recursive=False)
observer.start()

try:
    while observer.is_alive():
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()