from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins

from api.base.permissions import IsActiveUser
from api.v1.admin.recipe.filters import RecipeFilter
from api.v1.admin.recipe.serializers import AdminListRecipeSerializer, AdminUpdateRecipeSerializer, \
    AdminCreateRecipeSerializer
from api.v1.admin.recipe.swagger import recipe_create, recipe_update
from apps.recipe.models import Recipe
from base.pagination import BasePagination


class AdminPendingRecipeViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Recipe.objects.filter(moderation_status='Pending').all()
    serializer_class = AdminListRecipeSerializer
    permission_classes = [IsActiveUser]
    pagination_class = BasePagination
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.annotate(favorites_count=Count('favorited_by'))

    def get_serializer_class(self):
        if self.action == 'update':
            return AdminUpdateRecipeSerializer
        else:
            return AdminListRecipeSerializer

    @swagger_auto_schema(**recipe_update)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AdminApprovedRecipeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Recipe.objects.filter(moderation_status='Approved').all()
    serializer_class = AdminListRecipeSerializer
    permission_classes = [IsActiveUser]
    pagination_class = BasePagination
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.annotate(favorites_count=Count('favorited_by'))

    def get_serializer_class(self):
        if self.action == 'update':
            return AdminUpdateRecipeSerializer
        elif self.action == 'create':
            return AdminCreateRecipeSerializer
        else:
            return AdminListRecipeSerializer

    @swagger_auto_schema(**recipe_update)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(**recipe_create)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AdminRejectedRecipeViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Recipe.objects.filter(moderation_status='Rejected').all()
    serializer_class = AdminListRecipeSerializer
    permission_classes = [IsActiveUser]
    pagination_class = BasePagination
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.annotate(favorites_count=Count('favorited_by'))

    def get_serializer_class(self):
        if self.action == 'update':
            return AdminUpdateRecipeSerializer
        else:
            return AdminListRecipeSerializer

    @swagger_auto_schema(**recipe_update)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


