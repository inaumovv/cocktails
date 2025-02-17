from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.base.permissions import IsActiveUser
from api.v1.admin.statistics.serializers import AdminStatisticsSerializer


class AdminStatisticsViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AdminStatisticsSerializer
    permission_classes = [IsActiveUser]
