from django.db import models

# Create your models here.
from django.db import models


class Stage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    
    stage = models.ForeignKey(
        Stage, on_delete=models.CASCADE, related_name="leads")

    def __str__(self):
        return self.name
