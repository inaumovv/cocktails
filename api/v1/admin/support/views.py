from apps.channel.models import Ticket
from apps.user.models import User
from .serializers import AdminTicketListSerializer
from api.base.permissions import IsActiveUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response



class AdminTicketViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AdminTicketListSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        return Ticket.objects.all().order_by('-updated_at')

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminTicketListSerializer
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def last(self, request, *args, **kwargs):
        qs = self.get_queryset()
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)

        chat = qs.filter(user=user, status='open').first()

        return Response({
            'chat_id': chat.id,
        })