from my_runs.models import Run, Split
from rest_framework import viewsets
from .serializers import RunSerializer, SplitSerializer


class RunView(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    queryset = Run.objects.all()


class SplitView(viewsets.ModelViewSet):
    serializer_class = SplitSerializer
    queryset = Split.objects.all()


