from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    specialty = models.CharField(max_length=20)
    # certificate_details=models.TextField()
    # available_times = models.JSONField()
    