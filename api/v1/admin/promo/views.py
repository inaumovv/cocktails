import django_filters
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.base.permissions import IsActiveUser
from api.v1.admin.promo.filters import PromoFilter
from api.v1.admin.promo.serializers import AdminPromoSerializer, AdminPurchasedPromoSerializer
from api.v1.admin.promo.swagger import purchased_promo_get, purchased_promo_post
from apps.goods.models import Promo, PurchasedPromo
from apps.user.models import User
from base.pagination import BasePagination


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
    queryset = PurchasedPromo.objects.all()

    @swagger_auto_schema(**purchased_promo_get)
    def get(self, request, id, *args, **kwargs):
        search = request.query_params.get('search')

        queryset = PurchasedPromo.objects.filter(promo_id=id)

        if search:
            queryset = queryset.filter(
                Q(user_id__icontains=search) |
                Q(purchased_at__icontains=search)
            )

        # Сериализация и возврат данных
        serializer = AdminPurchasedPromoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**purchased_promo_post)
    def post(self, request, id, *args, **kwargs):
        user_id = request.data.get('user_id')

        try:
            Promo.objects.get(id=id)
        except Promo.DoesNotExist:
            return Response({"error": "Promo not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if PurchasedPromo.objects.filter(user_id=user_id, promo_id=id).exists():
            return Response({"error": "User already purchased this promo"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем купленный промокод
        purchased_promo = PurchasedPromo.objects.create(user_id=user_id, promo_id=id)

        # Сериализация и возврат данных
        serializer = AdminPurchasedPromoSerializer(purchased_promo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id, *args, **kwargs):
        """
        Удаляет купленный промокод по promo_id и user_id.
        """
        user_id = request.data.get('user_id')

        try:
            purchased_promo = PurchasedPromo.objects.get(promo_id=id, user_id=user_id)
        except PurchasedPromo.DoesNotExist:
            return Response({"error": "Purchased promo not found"}, status=status.HTTP_404_NOT_FOUND)

        purchased_promo.delete()
        return Response({"message": "Purchased promo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




