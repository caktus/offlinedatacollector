from rest_framework import serializers
from rest_framework.compat import get_model_name
from rest_framework.reverse import reverse

from . import models


class HATEOASMixin(object):
    """Serializer mixin for providing links."""

    def get_links(self, obj):
        """Related resources for the object."""
        request = self.context['request']
        detail_name = '{}-detail'.format(get_model_name(obj.__class__))
        return {
            'self': reverse(detail_name, kwargs={'pk': obj.pk}, request=request),
        }


class CleaningSerializer(HATEOASMixin, serializers.ModelSerializer):
    """Cleaning serialization."""

    completed = serializers.BooleanField(required=False, default=False)
    links = serializers.SerializerMethodField()

    class Meta:
        model = models.Cleaning
        fields = ('id', 'completed', 'date', 'links', )

    def validate_date(self, value):
        """Validate date/user uniqueness."""

        request = self.context['request']
        qs = models.Cleaning.objects.filter(user=request.user, date=value)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Record for this date already exists.')
        return value
