import json
import uuid
import requests

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, TemplateView, View

from .models import Camera
from .tasks import AI_CORE_IP
from .management.commands.startserver import DATA, DATA_LIST
# Create your views here.

MAX_PEOPLE_IN_STORE = 5

class IndexView(TemplateView):
    template_name = "crowdeye/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cameras"] = Camera.objects.count() 
        return context
    
    def post(self, request):
        global MAX_PEOPLE_IN_STORE
        MAX_PEOPLE_IN_STORE = request.POST['max']
        return redirect('index')
    

class CamerasView(View):
    def get(self, request):
        context = {
            "cameras": Camera.objects.all(),
            "ai_core_ip": AI_CORE_IP
        }
        return render(request, "crowdeye/cameras.html", context=context)

    def post(self, request):
        # Test camera is pingable
        if (request.POST.get('dir', None) is not None):
            c = Camera.objects.get(node_id=request.POST['node_id'])
            c.rtl = request.POST['dir'] == ['rtl']
            c.save()
            return redirect("cameras")
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

        try:
            x = requests.post(AI_CORE_IP + "/" + "add_camera", json=data) # , headers=headers)
        except requests.exceptions.ConnectionError:
            pass
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
            DATA[node_id]
        )

class ApiGlobalView(View):
    def get(self, request):
        # responses = [DATA[key] for key in DATA]
        responses = list(DATA.values())
        data = []
        num_people = 0
        total_in = 0
        total_out = 0
        for i in responses:
            data.append(i)
            rtl = Camera.objects.get(node_id=i['node_id']).rtl
            new = abs(i['crossed_left'] - i['crossed_right'])
            if rtl:
                new *= -1
            num_people += new
            total_in += i['crossed_left']
            total_out += i['crossed_right']
        return JsonResponse(
            {
                "max": MAX_PEOPLE_IN_STORE,
                "people_in_store": num_people,
                "total_in": total_in,
                "total_out": total_out,
                "data": data
            }
        )

class SimpleView(TemplateView):
    template_name = "crowdeye/simple.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MAX_PEOPLE_IN_STORE"] = MAX_PEOPLE_IN_STORE 
        return context
    


class ApiCLView(View):
    def post(self, request):
        pos = json.loads(request.body.decode('UTF-8'))
        print(pos)

        data = {
            'ax': pos[0][0],
            'ay': pos[0][1],
            'bx': pos[1][0],
            'by': pos[1][1],

        }
        headers = {'content-type': 'application/json'}

        x = requests.post(AI_CORE_IP +  "/change_line/" + str(pos[2]), json=data) # , headers=headers)

        return JsonResponse(
            {
                'a': 'b'
            }
        )

class ApiDELView(View):
    def get(self, request, node_id):
        x = requests.post(AI_CORE_IP +  "/reset_camera/" + str(node_id), json={}) # , headers=headers)

        return JsonResponse(
            {
                'a': 'b'
            }
        )


class DisplayView(TemplateView):
    template_name = "crowdeye/enter.html"
