from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime
import smtplib, ssl

username = "apoyopyc@epssanitas.com"
password = "jgsrifsigdxgivct"

#password = Practicante2021
def envioCorreoError(nombre_archivo,remitente,archivo_adjunto):

	# datos para iniciar sesion

	# datos envio correo
	destinatario = remitente

	# crear el mensaje
	mensaje = MIMEMultipart("alternative") # estandar
	mensaje["Subject"] = 'INCIDENCIA ARCHIVO COHORTES: '+ nombre_archivo
	mensaje["From"] = username
	mensaje["To"] = destinatario

	html = f"""
	<html>
	<body>
	<p style='font-size: 15px;'>
		buen dia
	</p>
	<p style='font-size: 12px;color: black;font-family: Arial, Helvetica, sans-serif;'>
		El presente correo es para informarte una incidencia con la información presentada con respecto al
		Sistema de Recepción de Cohortes.
	</p>
	<p>**********************************************************
	</p>
	<p style="font-size: 14px;font-family: Arial, Helvetica, sans-serif; color: red; font-weight: bold;" ;>
		Incidencias: </p>
	<p style="font-size: 14px;font-family: Arial, Helvetica, sans-serif; color: red; font-weight: bold;" ;>
		El archivo contiene errores de contenido en los datos, en este correo te adjuntamos el archivo con una
		columna de los errores. </p>
	<p>**********************************************************
	</p>
	<p style="font-size: 12px;font-family: Arial, Helvetica, sans-serif;">A continuacion una recopilacion de la
		informacion enviada</p>
	<p style="color: red;font-size: 12px; font-family: Arial, Helvetica, sans-serif;">-Nombre del archivo: {nombre_archivo}</p>
	<p style="color: red;font-size: 12px; font-family: Arial, Helvetica, sans-serif;">-Fecha del envió: {datetime.now()}</p>
	<p style="color: black;font-size: 12px; font-family: Arial, Helvetica, sans-serif;">¡Que tenga feliz día!</p>
	<p style="color: black
	; font-weight:bold ;font-size: 12px; font-family: Arial, Helvetica, sans-serif;">¡Por favor no responda a este
		correo, debe enviar el archivo nuevamente mediante el formulario!</p>

	</body>
	</html>
	"""
	# el contenido del mensaje como HTML
	parte_html = MIMEText(html, "html")
	# agregar ese contenido al mensaje
	mensaje.attach(parte_html)
	print(archivo_adjunto)
	archivo = archivo_adjunto

	with open(archivo, "rb") as adjunto:
		contenido_adjunto = MIMEBase("application", "octet-stream")
		contenido_adjunto.set_payload(adjunto.read())

	
	encoders.encode_base64(contenido_adjunto)


	contenido_adjunto.add_header(
		"Content-Disposition",
		f"attachment; filename= {archivo}"
	)

	mensaje.attach(contenido_adjunto)
	text = mensaje.as_string()

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(username, password)
		server.sendmail(username,destinatario,text)
		print("correo enviado")

def envioCorreoCorrecto(nombre_archivo,remitente):


	# datos para iniciar sesion

	# datos envio correo
	destinatario = remitente

	# crear el mensaje
	mensaje = MIMEMultipart("alternative") # estandar
	mensaje["Subject"] = 'ARCHIVO CARGADO CORRECTAMENTE: ' + nombre_archivo
	mensaje["From"] = username
	mensaje["To"] = destinatario

	html = f"""
	<html>
	<body>
		<p style='font-size: 12px;font-family: Arial, Helvetica, sans-serif;'>
			buen dia
		</p>
		<p style='font-size: 12px;color: #00CF07;font-weight: bold; font-family: Arial, Helvetica, sans-serif;'>
			El presente correo es para notificarte que el archivo pasó la segunda fase de validación (Validación de Información) correctamente.
		</p>
		<p style='font-size: 12px; font-family: Arial, Helvetica, sans-serif;'>A continuacion una recopilacion de la
			informacion enviada</p>
		<p style='color: #FF0000;font-family: Arial, Helvetica, sans-serif; font-size: 12px;'>-Nombre del archivo: {nombre_archivo}</p>
		<p style='color: #FF0000; font-family: Arial, Helvetica, sans-serif; font-size: 12px;'>-Fecha del envió: {datetime.now()}</p>
		<p style='font-family: Arial, Helvetica, sans-serif;font-size: 12px;' ;>¡Que tenga feliz día!</p>
	</body>
	</html>
	"""
	
	# el contenido del mensaje como HTML
	parte_html = MIMEText(html, "html")
	# agregar ese contenido al mensaje
	mensaje.attach(parte_html)

	text = mensaje.as_string()
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(username, password)
		server.sendmail(username,destinatario,text)
		print("correo enviado")

def envioCorreo_archivonopermitido(nombre_archivo,remitente):


	# datos para iniciar sesion

	# datos envio correo
	destinatario = remitente

	# crear el mensaje
	mensaje = MIMEMultipart("alternative") # estandar
	mensaje["Subject"] = 'Archivo correcto'
	mensaje["From"] = username
	mensaje["To"] = destinatario

	html = f"""
	<body>
		Hola {destinatario}<br>
		<p style='font-size: 17px;color: red;font-weight: bold;'>
		El Presente correo es para notificarle que el archivo tiene incidencias en la informacion.
		</p>
		<p style='font-size: 15px; color: red;'>El archivo debe tener formato xlsx</p>
		<p style='color: blue;'>-Nombre del archivo: {nombre_archivo}</p>
		<p style='color: blue;'>-Fecha del envió: {datetime.now()}</p>
		<p style='font-weight: bold';>¡Que tenga feliz día!</p>

	</body>
	</html>
	"""
	
	# el contenido del mensaje como HTML
	parte_html = MIMEText(html, "html")
	# agregar ese contenido al mensaje
	mensaje.attach(parte_html)

	text = mensaje.as_string()
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(username, password)
		server.sendmail(username,destinatario,text)
		print("correo enviado")
		