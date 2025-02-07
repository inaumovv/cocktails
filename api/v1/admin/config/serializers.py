from rest_framework import serializers
from apps.common.models import Config

__all__ = [
    'AdminListConfigSerializer',
]


class AdminListConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Config
        fields = '__all__'