from rest_framework import serializers
from .models import Stage, Lead





class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'phone', 'stage']

class StageSerializer(serializers.ModelSerializer):
    # leads = serializers.StringRelatedField(many=True,read_only=True)
    leads = LeadSerializer(many=True, read_only=True)

    class Meta:
        model = Stage
        fields = ['id', 'name','leads']