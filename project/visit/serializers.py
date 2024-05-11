'''
from django.db import models

# Create your models here.
Visit
   
Measurement

class Attachment(models.Model):

'''

from rest_framework import serializers
from .models import *

class MeasurementSerializer(serializers.Serializer):
    height = serializers.CharField(max_length=255 ,required=False)
    weight = serializers.CharField(max_length=255 ,required=False)
    blood_pressure = serializers.CharField(max_length=255 ,required=False)
    temperature = serializers.CharField(max_length=255 ,required=False)
    pulse = serializers.CharField(max_length=255 ,required=False)
    oxygen_level = serializers.CharField(max_length=255 ,required=False)
    
class AttachmentSerializer(serializers.ModelSerializer):
    file_type=serializers.CharField(read_only=True)
    class Meta:
        model = Attachment
        # fields = '__all__'
        exclude = ['is_deleted']

class VisitSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer( required=False)
    attachment = AttachmentSerializer( read_only=True, many=True,source='visit_attachments', required=False)
    class Meta:
        model = Visit
        # fields = '__all__'
        exclude = ['is_deleted']


class StatisticsSerializer(serializers.Serializer):
    total_visits=serializers.IntegerField()
    total_patients=serializers.IntegerField()
    total_doctors=serializers.IntegerField()
    total_employees=serializers.IntegerField()