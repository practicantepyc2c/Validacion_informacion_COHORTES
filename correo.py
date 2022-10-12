from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime
import smtplib, ssl

username = "practicante_pyc2_c@epssanitas.com"
password = "lqvnyepbtszlzxfp"

#password = Practicante2021
def envioCorreoError(nombre_archivo):

	# datos para iniciar sesion

	# datos envio correo
	destinatario = "practicante_pyc2_c@epssanitas.com"

	# crear el mensaje
	mensaje = MIMEMultipart("alternative") # estandar
	mensaje["Subject"] = 'Archivo incorrecto'
	mensaje["From"] = username
	mensaje["To"] = destinatario

	html = f"""
	<html>
	<body>
		Hola {destinatario}<br>
		<p style='font-size: 17px;color: red;font-weight: bold;'>
		El Presente correo es para notificarle que el archivo tiene incidencias en la informacion.
		</p>
		<p style='font-size: 15px; color: red;'>El correo tiene un adjunto con el reporte de los errores</p>
		<p style='font-size: 15px;'>A continuacion una recopilacion de la informacion enviada</p>
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

	archivo = "Archivo-errores.xlsx"

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

def envioCorreoCorrecto(nombre_archivo):


	# datos para iniciar sesion

	# datos envio correo
	destinatario = "practicante_pyc2_c@epssanitas.com"

	# crear el mensaje
	mensaje = MIMEMultipart("alternative") # estandar
	mensaje["Subject"] = 'Archivo correcto'
	mensaje["From"] = username
	mensaje["To"] = destinatario

	html = f"""
	<html>
	<body>
		<body>
		<p style='font-size: 20px;'>
		buen dia
		</p>
		<p style='font-size: 17px;color: rgb(135, 221, 5);font-weight: bold;'>
		El Presente correo es para notificarle que el archivo fue verificado correctamente y no tiene ningun
		error.
		</p>
		<p style='font-size: 15px;'>A continuacion una recopilacion de la informacion enviada</p>
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
