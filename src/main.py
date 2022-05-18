from os import getenv
from dotenv import load_dotenv
import requests
import Baq
import status_changed

def main() -> None:
	response = requests.get(Baq.URL)
	response = response.content.decode()
	status = Baq.parse_status(response)
	prev_status = Baq.get_prev_status()

	if status == prev_status:
		Baq.save_prev_status(status)
		status_changed.notify(status, prev_status)

if __name__ == '__main__':
	load_dotenv()
	main()
