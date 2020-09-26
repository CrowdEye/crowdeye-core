from background_task import background
from .models import Camera
from .views import AI_CORE_IP

@background(schedule=1)
def check_cams():
    print(f"Syncing cams: we have {Camera.objects.count()} cameras")
    x = requests.get(AI_CORE_IP + "/" + "get_cameras")
    print(x)
    # for cam in Camera.objects.all()
    #     x = requests.get(AI_CORE_IP + "/" + "remove_camera" + "/" + cam.node_id)

check_cams(repeat=1, repeat_until=None)