import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from background_task import background
from .models import Camera

AI_CORE_IP = "http://127.0.0.1:5500"


DATA = {}

@background()
def check_cams():
    print(".", end="", flush=True)

    retry_strategy = Retry(
        total=3,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    x = http.get(AI_CORE_IP + "/" + "get_cameras")
    if (len(x.json()) == Camera.objects.count()):  # Assume sets are equal
        return 
    res = x.json()
    print(res)

    # They have dangling cams
    for node_id in res:
        try:
            qs = Camera.objects.get(node_id=node_id)
        except Camera.DoesNotExist:
            print("Removing a camera")
            x = requests.delete(AI_CORE_IP + "/" + "remove_camera" + "/" + node_id)
    
    # We have extra cams
    for cam in Camera.objects.all():
        if (cam.node_id not in res):
            data = {
                'cam_ip': cam.url,
                'node_id': str(cam.node_id)
            }
            headers = {'content-type': 'application/json'}
            
            print("Adding a camera")
            x = requests.post(AI_CORE_IP + "/" + "add_camera", json=data)

# @background()
# def get_cams():
#     all_cams = []
#     print("-", end="", flush=True)
#     x = requests.get(AI_CORE_IP + "/" + "get_cameras")
#     data = x.json()
#     # print(data)

#     for node_id in data:
#         x = requests.get(AI_CORE_IP + "/" + "camera" + "/" + node_id)
#         DATA[node_id] = x.json()

check_cams(repeat=25, repeat_until=None)
# get_cams(repeat=5, repeat_until=None)
