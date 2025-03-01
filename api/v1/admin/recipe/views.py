from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from .serializers import *
from base.pagination import BasePagination
from rest_framework.permissions import AllowAny
from apps.recipe.models import *
from rest_framework.decorators import action
from django.http import QueryDict
import json


class RecipeViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    pagination_class = BasePagination
    serializer_class = AdminRecipeSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminRecipeSerializer
        elif self.action == 'retrieve':
            return AdminRecipeSerializer
        elif self.action == 'create':
            return AdminCreateRecipeSerializer
        elif self.action in ['update', 'partial_update']:
            return AdminUpdateRecipeSerializer
        return AdminRecipeSerializer

    def list(self, request, *args, **kwargs):
        qs = super().get_queryset()
        pending_recipes = qs.filter(moderation_status='Pending')

        data = {
            'all': AdminRecipeSerializer(qs, many=True).data,
            'pending': AdminRecipeSerializer(pending_recipes, many=True).data,
        }

        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print('partial_update')
        print(partial)
        print(request.data)
        serializer = AdminUpdateRecipeSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print('update')
        print(request.data)
        # serializer = self.get_serializer(instance, data=request.data)

        data = request.data

        if isinstance(data, QueryDict):
            data = data.dict()

            for key in data:
                if key == 'tools' and isinstance(data[key], str):
                    clean_tools = data[key].strip('[]')
                    data[key] = list(map(int, clean_tools.split(','))) if clean_tools else []

                elif key == 'ingredients' and isinstance(data[key], str):
                    ingredients_json = f'[{data["ingredients"]}]'
                    data[key] = json.loads(ingredients_json)

                elif key == 'isEnabled' and isinstance(data[key], str):
                    data[key] = data[key].lower() == 'true'

                elif key == 'user' and isinstance(data[key], str):
                    data[key] = int(data[key])

                elif key == 'instruction' and isinstance(data[key], str):
                    clean_instruction = data[key].replace('\t', '').replace('\n', '')
                    try:
                        data[key] = json.loads(clean_instruction)
                    except json.JSONDecodeError:
                        data[key] = {}

                elif key == 'photo':
                    pass

                else:
                    data[key] = data[key].replace('"', '')

        print(data)

        serializer = self.get_serializer(instance, data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = AdminCreateRecipeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(AdminRecipeSerializer(recipe, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = AdminRecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data)
