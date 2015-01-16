from rest_framework import viewsets

from . import models, serializers


class CleaningViewSet(viewsets.ModelViewSet):
    """BREAD operations for team members."""

    model = models.Cleaning
    serializer_class = serializers.CleaningSerializer
    ordering_fields = ('date', )

    def get_queryset(self):
        return self.request.user.cleanings.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
