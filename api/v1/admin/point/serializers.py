from rest_framework import serializers
from apps.user.models import Point
from apps.recipe.models import *
from api.v1.admin.profile.serializers import AdminUserListSerializer

__all__ = [
    'AdminListPointSerializer',
]


class AdminListPointSerializer(serializers.ModelSerializer):
    user = AdminUserListSerializer(many=False, read_only=True)

    class Meta:
        model = Point
        fields = '__all__'