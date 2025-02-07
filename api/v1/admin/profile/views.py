from apps.user.models import User
from apps.recipe.models import *
from .serializers import AdminUserSerializer, AdminUserListSerializer, AdminUserUpdateSerializer, AdminUserCreateSerializer
from api.base.permissions import IsActiveUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status


class AdminUserViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [IsActiveUser]
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminUserListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AdminUserSerializer
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = request.data.get('partial', False)
        user = self.get_object()
        serializer = AdminUserUpdateSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = AdminUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.save()
        return Response(AdminUserSerializer(user).data, status=status.HTTP_201_CREATED)