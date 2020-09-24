from django.db import models

# Create your models here.
class Camera(models.Model):
    url = models.CharField(max_length=4096)
    node_id = models.CharField(max_length=4096)

    def __str__(self):
        return self.url
