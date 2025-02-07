from rest_framework import serializers
from apps.channel.models import Ticket
from api.v1.admin.profile.serializers import AdminUserListSerializer

__all__ = [
    'AdminTicketListSerializer',
]


class AdminTicketListSerializer(serializers.ModelSerializer):
    user = AdminUserListSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'