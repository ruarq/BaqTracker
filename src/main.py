from enum import Enum, auto
from os import getenv
from typing import Any
from dotenv import load_dotenv
import requests
import smtplib, ssl

PREV_STATUS_FILENAME = 'prev_status.txt'

UNKNOWN_STR = 'Unbekannt'
NOT_AVAIL_STR = 'Nicht verfügbar'
AVAIL_STR = 'Verfügbar'
LIMITED_STR = 'Limitierter Bestand'

class Status(Enum):
	UNKNOWN = auto()
	NOT_AVAIL = auto()
	AVAIL = auto()
	LIMITED = auto()

	def __str__(self) -> str:
		if self.value == self.NOT_AVAIL:
			return NOT_AVAIL_STR
		elif self.value == self.AVAIL:
			return AVAIL_STR
		elif self.value == self.LIMITED:
			return LIMITED_STR
		else:
			return UNKNOWN_STR

	def __eq__(self, other) -> bool:
		if isinstance(other, int):
			return self.value == other

		if isinstance(other, Status):
			return self is other

		return False

def get_status(s: str) -> Status:
	if 'Noch keine abschätzbare Lieferzeit' in s:
		return Status.NOT_AVAIL
	elif 'Auf Lager' in s:
		return Status.AVAIL
	elif 'Limitierter Bestand' in s:
		return Status.LIMITED
	else:
		return Status.UNKNOWN

def get_prev_status() -> Status:
	try:
		with open(PREV_STATUS_FILENAME, 'r') as f:
			stat_str = f.readline()
			if stat_str == NOT_AVAIL_STR:
				return Status.NOT_AVAIL
			elif stat_str == AVAIL_STR:
				return Status.AVAIL
			elif stat_str == LIMITED_STR:
				return Status.LIMITED
			else:
				return Status.UNKNOWN
		
	except FileNotFoundError:
		with open(PREV_STATUS_FILENAME, 'w') as f:
			f.write(str(Status.UNKNOWN))
			return Status.UNKNOWN

def save_prev_status(status: Status):
	with open(PREV_STATUS_FILENAME, 'w') as f:
		f.write(status)

def send_mail(recipient: str, subject: str, msg: str) -> None:
	host = getenv('EMAIL_HOST')
	mail = getenv('EMAIL_ADDRESS')
	psw = getenv('EMAIL_PASSWORD')
	port = int(getenv('EMAIL_PORT'))

	# prep msg
	msg = f'From: {mail}\nSubject: {subject}\n\n{msg}'.encode('utf-8')

	ctx = ssl.create_default_context()
	with smtplib.SMTP_SSL(host, port, context=ctx) as server:
		server.login(mail, psw)
		server.sendmail(mail, recipient, msg)

def main() -> None:
	url = 'https://www.airpaq.de/collections/alle-produkte/products/turnbeutel-baq?variant=40697128321135'
	response = requests.get(url)
	response = response.content.decode()
	status = get_status(response)
	prev_status = get_prev_status()

	if status != prev_status:
		recipient_name = getenv('RECIPIENT_NAME')
		recipient_mail = getenv('RECIPIENT_MAIL')
		message = f"Hallo {recipient_name},\n\nder Status von 'Turnbeutel Baq' hat sich von '{prev_status}' zu '{status}' geändert."
		subject = "'Turnbeutel Baq' Status hat sich geändert"
		send_mail(recipient_mail, subject, message)
		save_prev_status(status)

if __name__ == '__main__':
	load_dotenv()
	main()
