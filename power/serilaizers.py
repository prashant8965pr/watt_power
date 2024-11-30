
from rest_framework import serializers
from .models import SpeedLevel


class SpeedSerializers(serializers.ModelSerializer):
    class Meta:
        model = SpeedLevel
        fields = '__all__'