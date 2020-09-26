import uuid
import requests


from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, TemplateView, View

from .models import Camera
# Create your views here.

AI_CORE_IP = "http://198.84.180.114:5500"

class IndexView(TemplateView):
    template_name = "crowdeye/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cameras"] = Camera.objects.count() 
        return context
    

class CamerasView(View):
    def get(self, request):
        context = {
            "cameras": Camera.objects.all(),
            "ai_core_ip": AI_CORE_IP
        }
        return render(request, "crowdeye/cameras.html", context=context)

    def post(self, request):
        # Test camera is pingable
        try:
            x = requests.head(request.POST['url'], timeout=2)  # get only headers, not stream
        except requests.exceptions.ConnectionError:
            print('Error pinging cam')
            messages.warning(request, "Camera doesn't seem to exists")
            return redirect("cameras")
        

        messages.success(request, 'Added camera.')
        # node_id = uuid.uuid4()
        node_id = Camera.objects.count() + 1
        try:
            Camera.objects.create(url=request.POST['url'], node_id=node_id)
        except requests.exceptions.MissingSchema:
            print('Malformed url')
            messages.warning(request, "You forgot to add `http://` or `https://` to your url")
            return redirect("cameras")


        data = {
            'cam_ip': request.POST['url'],
            'node_id': str(node_id)
        }
        headers = {'content-type': 'application/json'}

        x = requests.post(AI_CORE_IP + "/" + "add_camera", json=data) # , headers=headers)

        return redirect("cameras")

class CameraDeleteView(DeleteView):
    model = Camera
    template_name = "camera_delete.html"
    success_url = reverse_lazy('cameras')

    def delete(self, *args, **kwargs):

        x = requests.delete(AI_CORE_IP + "/" + "remove_camera" + "/" + Camera.objects.get(pk=kwargs['pk']).node_id)

        return super(CameraDeleteView, self).delete(*args, **kwargs)



class ApiView(View):
    def get(self, request, node_id):
        x = requests.get(AI_CORE_IP + "/" + "camera" + "/" + node_id)
        return JsonResponse(
            x.json()
        )