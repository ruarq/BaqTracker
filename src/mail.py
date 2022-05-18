import smtplib, ssl
from os import getenv
from Baq import Status

def send(status: Status, prev_status: Status) -> None:
	recipient_name = getenv('RECIPIENT_NAME')
	recipient_mail = getenv('RECIPIENT_MAIL')
	msg = f"Hallo {recipient_name},\n\nder Status von 'Turnbeutel Baq' hat sich von '{prev_status}' zu '{status}' geändert."
	subject = "'Turnbeutel Baq' Status hat sich geändert"
	
	host = getenv('EMAIL_HOST')
	port = int(getenv('EMAIL_PORT'))
	mail = getenv('EMAIL_ADDRESS')
	psw = getenv('EMAIL_PASSWORD')

	# prep msg
	msg = f'From: {mail}\nSubject: {subject}\n\n{msg}'.encode('utf-8')

	ctx = ssl.create_default_context()
	with smtplib.SMTP_SSL(host, port, context=ctx) as server:
		server.login(mail, psw)
		server.sendmail(mail, recipient_mail, msg)
