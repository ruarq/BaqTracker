from os import getenv
from Baq import Status
import mail

def notify(status: Status, prev_status: Status):
	mail.send(status, prev_status)
