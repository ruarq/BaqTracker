from enum import Enum, auto

URL = 'https://www.airpaq.de/collections/alle-produkte/products/turnbeutel-baq?variant=40697128321135'
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

def parse_status(s: str) -> Status:
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
		f.write(str(status))
