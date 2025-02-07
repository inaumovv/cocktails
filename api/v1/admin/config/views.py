from apps.common.models import Config
from .serializers import AdminListConfigSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins


class AdminConfigViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Config.objects.all()
    serializer_class = AdminListConfigSerializer
