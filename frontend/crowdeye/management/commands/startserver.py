import time
import threading
import requests

from django.core.management.base import BaseCommand, CommandError
from django.core.management import execute_from_command_line


from ...tasks import AI_CORE_IP

DATA = {}
DATA_LIST = []

def get_cams():
    global DATA_LIST
    global DATA
    while True:
        try:
            all_cams = []
            print("-", end="", flush=True)
            x = requests.get(AI_CORE_IP + "/" + "get_cameras")
            data = x.json()

            print(data)

            temp = []
            for node_id in data:
                x = requests.get(AI_CORE_IP + "/" + "camera" + "/" + node_id)
                tmp = x.json()
                DATA[node_id] = tmp
                temp.append(tmp)
            DATA_LIST = temp

            # globals()['DATA_LIST'] = temp

            print('t', DATA_LIST)

            time.sleep(2)
        except Exception as e:
            print(f"ERROR: {e}")
            print(e.with_traceback())


class Command(BaseCommand):
    help = '.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting'))

        x = threading.Thread(target=get_cams)
        x.setDaemon(True)

        x.start()

        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5520'])



