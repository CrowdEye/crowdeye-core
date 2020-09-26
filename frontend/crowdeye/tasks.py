import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from background_task import background
from .models import Camera
from .views import AI_CORE_IP

@background(schedule=25)
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

check_cams(repeat=25, repeat_until=None)