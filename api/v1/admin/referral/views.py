import django_filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from api.base.permissions import IsActiveUser
from api.v1.admin.referral.filters import ReferralFilter
from api.v1.admin.referral.serializers import UserReferralSerializer, ReferralSerializer
from apps.user.models import User
from base.pagination import BasePagination


class ReferralAdminViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserReferralSerializer
    permission_classes = [IsActiveUser, DjangoModelPermissions]
    queryset = User.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ReferralFilter
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReferralSerializer
        return super().get_serializer_class()

