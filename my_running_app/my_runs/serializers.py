from rest_framework import serializers
from .models import Run, Split


class SplitSerializer(serializers.ModelSerializer):
  class Meta:
    model = Split
    fields = ('split_number', 'elapsed_time', 'moving_time')


class RunSerializer(serializers.ModelSerializer):
  splits = SplitSerializer(many=True)

  class Meta:
    model = Run
    fields = ('id', 'name', 'date', 'distance', 'duration', 'splits')

