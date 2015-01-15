from rest_framework import viewsets

from . import models, serializers


class CleaningViewSet(viewsets.ModelViewSet):
    """BREAD operations for team members."""

    queryset = models.Cleaning.objects.all()
    serializer_class = serializers.CleaningSerializer
    filter_fields = ('user', )
    search_fields = ('user', )
    ordering_fields = ('user', )
