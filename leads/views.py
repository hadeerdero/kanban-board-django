from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Stage, Lead
from .serializers import StageSerializer, LeadSerializer


class StageViewSet(ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer


class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
