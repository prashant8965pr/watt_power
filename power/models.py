from django.db import models

# Create your models here.
class SpeedLevel(models.Model):
    speed = models.FloatField()
    start_time = models.DateTimeField(auto_now_add=True)