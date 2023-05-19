from time import sleep
from server import run_server
from services import get_system_status

run_server()
while True:
    get_system_status()
    sleep(300)
