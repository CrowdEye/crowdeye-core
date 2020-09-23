from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, TemplateView, View

from .models import Camera
# Create your views here.
class IndexView(TemplateView):
    template_name = "crowdeye/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cameras"] = Camera.objects.count() 
        return context
    

class CamerasView(View):
    def get(self, request):
        context = {
            "cameras": Camera.objects.all()
        }
        return render(request, "crowdeye/cameras.html", context=context)

    def post(self, request):
        print(request.POST)
        messages.success(request, 'Added camera.')
        Camera.objects.create(url=request.POST['url'])
        return redirect("cameras")

class CameraDeleteView(DeleteView):
    model = Camera
    template_name = "camera_delete.html"
    success_url = reverse_lazy('cameras')

