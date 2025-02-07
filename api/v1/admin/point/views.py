from apps.user.models import Point, User
from .serializers import AdminListPointSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.exceptions import ValidationError


class AdminPointViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Point.objects.all()
    serializer_class = AdminListPointSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')

        if not user_id:
            raise ValidationError({'user': 'User ID is required.'})

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError({'user': 'User with this ID does not exist.'})

        serializer.save(user=user)