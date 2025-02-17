import django_filters
from django.db.models import Q
from rest_framework import mixins, viewsets, status
from rest_framework.pagination import BasePagination
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.base.permissions import IsActiveUser
from api.v1.admin.promo.filters import PromoFilter
from api.v1.admin.promo.serializers import AdminPromoSerializer, AdminPurchasedPromoSerializer
from apps.goods.models import Promo, PurchasedPromo
from apps.user.models import User


class PromoAdminViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = AdminPromoSerializer
    permission_classes = [IsActiveUser, DjangoModelPermissions]
    queryset = Promo.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PromoFilter
    pagination_class = BasePagination


class PromoPurchasedAdminView(APIView):
    pagination_class = BasePagination
    permission_classes = [IsActiveUser, DjangoModelPermissions]

    def get(self, request, promo_id, *args, **kwargs):
        search = request.query_params.get('search')

        queryset = PurchasedPromo.objects.filter(promo_id=promo_id)

        if search:
            queryset = queryset.filter(
                Q(user_id__icontains=search) |
                Q(purchased_at__icontains=search)
            )

        # Сериализация и возврат данных
        serializer = AdminPurchasedPromoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, promo_id, *args, **kwargs):
        user_id = request.data.get('user_id')

        try:
            Promo.objects.get(id=promo_id)
        except Promo.DoesNotExist:
            return Response({"error": "Promo not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if PurchasedPromo.objects.filter(user_id=user_id, promo_id=promo_id).exists():
            return Response({"error": "User already purchased this promo"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем купленный промокод
        purchased_promo = PurchasedPromo.objects.create(user_id=user_id, promo_id=promo_id)

        # Сериализация и возврат данных
        serializer = AdminPurchasedPromoSerializer(purchased_promo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, promo_id, *args, **kwargs):
        """
        Удаляет купленный промокод по promo_id и user_id.
        """
        user_id = request.data.get('user_id')

        try:
            purchased_promo = PurchasedPromo.objects.get(promo_id=promo_id, user_id=user_id)
        except PurchasedPromo.DoesNotExist:
            return Response({"error": "Purchased promo not found"}, status=status.HTTP_404_NOT_FOUND)

        purchased_promo.delete()
        return Response({"message": "Purchased promo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




