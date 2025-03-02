from rest_framework import viewsets
from .serializers import HighlightMediaSerializer, HighlightSerializer
from .models import HighlightMedia, Highlight


class HighlightViewSet(viewsets.ModelViewSet):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer


class HighlightMediaViewSet(viewsets.ModelViewSet):
    queryset = HighlightMedia.objects.all()
    serializer_class = HighlightSerializer
