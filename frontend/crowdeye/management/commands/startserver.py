import time
import threading
import requests

from ...influx import *

from django.core.management.base import BaseCommand, CommandError
from django.core.management import execute_from_command_line


from ...tasks import AI_CORE_IP

DATA = {}
DATA_LIST = []
printedWriteError = False

def get_cams():
    global DATA_LIST
    global DATA
    global printedWriteError
    
    while True:
        try:
            # Try getting the cameras
            all_cams = []
            # print("-", end="", flush=True)
            # Make a call to the api for all of the camera data
            x = requests.get(AI_CORE_IP + "/" + "get_cameras")
            # Put the data into a variable
            data = x.json()

            # print(data)

            temp = []
            # Itterate over the data and construct it into an array of dicts
            for node_id in data:
                x = requests.get(AI_CORE_IP + "/" + "camera" + "/" + node_id)
                tmp = x.json()
                DATA[node_id] = tmp
                temp.append(tmp)
            DATA_LIST = temp

            # print('t', DATA_LIST)
            
            # Try to write to the database
            try:
                writeEntry(**DATA_LIST[0])
            except:
                if not printedWriteError:
                    print(":(")
                    printedWriteError = True

            time.sleep(2)
        except Exception as e:
            print(f"ERROR: {e}")
            print(e)


class Command(BaseCommand):
    help = '.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting'))

        x = threading.Thread(target=get_cams)
        x.setDaemon(True)

        x.start()

        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5510'])



