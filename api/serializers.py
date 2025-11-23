from rest_framework import serializers
from .models import Dataset

class SummarySerializer(serializers.Serializer):
    total_equipment = serializers.IntegerField()
    average_flowrate = serializers.FloatField()
    average_pressure = serializers.FloatField()
    average_temperature = serializers.FloatField()
    type_distribution = serializers.DictField(child=serializers.IntegerField())

class DatasetSerializer(serializers.ModelSerializer):
    summary = SummarySerializer(source='summary_json')

    class Meta:
        model = Dataset
        fields = ('id', 'file_name', 'upload_time', 'summary')
