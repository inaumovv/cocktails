from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import QueryDict
from apps.reaction.models import Claim
from apps.user.models import Point
from apps.common.models import Config
from .serializers import *
from django.contrib.contenttypes.models import ContentType
import json
from rest_framework.parsers import MultiPartParser, JSONParser
from base.pagination import BasePagination
from rest_framework.permissions import AllowAny
from .swagger import *
from apps.recipe.models import *
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from .filters import RecipeFilterSet
from django.http import Http404

from ...base.permissions import IsActiveUser


class LanguageFilterMixin:
    def get_language(self):
        return self.request.headers.get('User-Language', 'rus')

    def filter_by_language(self, qs):
        language = self.get_language()
        if language == 'rus':
            return qs.filter(language='RUS')
        return qs.filter(language='ENG')


class IngredientCategorySectionViewSet(LanguageFilterMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = IngredientCategorySection.objects.prefetch_related('categories__ingredients')
    serializer_class = IngredientCategorySectionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        return self.filter_by_language(qs)

    @swagger_auto_schema(**ingredient_category_block_list)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        query = self.request.query_params.get('q')

        if query:
            for block in response.data:
                filtered_categories = []
                for category in block['categories']:
                    filtered_ingredients = [ingredient for ingredient in category['ingredients'] if
                                            query.lower() in ingredient['name'].lower()]
                    if filtered_ingredients:
                        category['ingredients'] = filtered_ingredients
                        filtered_categories.append(category)
                block['categories'] = filtered_categories

        return response


class IngredientCategoryViewSet(LanguageFilterMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = IngredientCategory.objects.prefetch_related('ingredients')
    serializer_class = IngredientCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()

        qs = self.filter_by_language(qs)

        category_id = self.request.query_params.get('id')
        if category_id:
            qs = qs.filter(id=category_id)

        query = self.request.query_params.get('q')

        if query:
            qs = qs.filter(
                Q(ingredients__name__icontains=query)
            ).distinct()

        return qs

    @swagger_auto_schema(**ingredient_category_list)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class IngredientViewSet(LanguageFilterMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        return self.filter_by_language(qs)

    @swagger_auto_schema(**ingredient_retrieve)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ToolViewSet(LanguageFilterMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Tool.objects.all()
    serializer_class = ViewToolSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        return self.filter_by_language(qs)

    @swagger_auto_schema(**tool_list)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**tool_retrieve)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class RecipeViewSet(LanguageFilterMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Recipe.objects.filter(moderation_status='Approved')
    permission_classes = [AllowAny]
    pagination_class = BasePagination
    serializer_class = RecipeListSerializer
    filterset_class = RecipeFilterSet
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_by_language(queryset)
        queryset = queryset.annotate(popularity=Count('favorited_by'))

        return queryset

    def filter_for_selection(self, request, *args, **kwargs):
        main_ingredient = request.query_params.get('ingredients')
        ingredients = request.query_params.get('other_ingredients')

        try:
            main_ingredient_ids = [int(v) for v in main_ingredient.replace('-', ',').split(',')]
        except:
            return {}, 'No main ingredient ids provided.', status.HTTP_400_BAD_REQUEST

        try:
            ingredient_ids = [int(v) for v in ingredients.replace('-', ',').split(',')]
        except:
            return {}, 'No other ingredient ids provided.', status.HTTP_400_BAD_REQUEST

        if not main_ingredient_ids:
            return {}, "No main ingredient ids provided.", status.HTTP_400_BAD_REQUEST

        qs = self.get_queryset().select_related('user').prefetch_related(
            'recipe_ingredients__ingredient'
        )

        recipes_with_ingr = qs.filter(
            recipe_ingredients__ingredient__id__in=main_ingredient_ids
        ).distinct()

        recipes_with_main = recipes_with_ingr.annotate(
            matched_main_ingredients=Count('recipe_ingredients__ingredient__id',
                                           filter=Q(recipe_ingredients__ingredient__id__in=main_ingredient_ids),
                                           distinct=True)
        ).filter(matched_main_ingredients=len(main_ingredient_ids))

        if ingredient_ids:
            recipes_with_all_ingredients = recipes_with_main.filter(
                recipe_ingredients__ingredient__id__in=ingredient_ids
            ).annotate(
                matched_ingredients=Count('recipe_ingredients__ingredient__id',
                                          filter=Q(recipe_ingredients__ingredient__id__in=ingredient_ids),
                                          distinct=True)
            ).filter(matched_ingredients=len(ingredient_ids)).distinct()

            recipes_with_some_ingredients = recipes_with_main.filter(
                recipe_ingredients__ingredient__id__in=ingredient_ids
            ).annotate(
                matched_ingredients=Count('recipe_ingredients__ingredient__id',
                                          filter=Q(recipe_ingredients__ingredient__id__in=ingredient_ids),
                                          distinct=True)
            ).exclude(id__in=recipes_with_all_ingredients.values('id')).distinct().order_by('-matched_ingredients')

            for recipe in recipes_with_some_ingredients:
                missing_ingredients = list(set(ingredient_ids) - set(
                    recipe.recipe_ingredients.filter(ingredient__id__in=ingredient_ids).values_list('ingredient_id',
                                                                                                    flat=True)
                ))
                missing_ingredients_details = Ingredient.objects.filter(id__in=missing_ingredients)
                missing_ingredients_serialized = IngredientSerializer(missing_ingredients_details, many=True).data
                recipe.missing_ingredients = missing_ingredients_serialized
                recipe.missing_ingredients_count = missing_ingredients_details.count()
        else:
            recipes_with_all_ingredients = recipes_with_main
            recipes_with_some_ingredients = []

        serializer_all = SelectionRecipeSerializer(recipes_with_all_ingredients, many=True,
                                                   context={'request': request})
        serializer_some = SelectionRecipeSerializer(recipes_with_some_ingredients, many=True,
                                                    context={'request': request})

        return {
            'all_ingredients': serializer_all.data,
            'some_ingredients': serializer_some.data
        }, None, None

    @swagger_auto_schema(**recipe_list)
    def list(self, request, *args, **kwargs):
        if 'other_ingredients' in self.request.query_params:
            data, error, code = self.filter_for_selection(request, *args, **kwargs)
            if error:
                return Response({"detail": error}, status=code)
            return Response(data)
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**recipe_update)
    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop('partial', False)
        serializer = UpdateRecipeSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @swagger_auto_schema(**recipe_delete)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(**recipe_selection)
    @action(detail=False, methods=['post'])
    def selection(self, request):
        main_ingredient_ids = request.data.get('main_ingredients', [])
        ingredient_ids = request.data.get('other_ingredients', [])

        if not main_ingredient_ids:
            return Response({"detail": "No main ingredient ids provided."}, status=status.HTTP_400_BAD_REQUEST)

        qs = self.get_queryset().select_related('user').prefetch_related(
            'recipe_ingredients__ingredient'
        )

        recipes_with_ingr = qs.filter(
            recipe_ingredients__ingredient__id__in=main_ingredient_ids
        ).distinct()

        recipes_with_main = recipes_with_ingr.annotate(
            matched_main_ingredients=Count('recipe_ingredients__ingredient__id',
                                           filter=Q(recipe_ingredients__ingredient__id__in=main_ingredient_ids),
                                           distinct=True)
        ).filter(matched_main_ingredients=len(main_ingredient_ids))

        if ingredient_ids:
            recipes_with_all_ingredients = recipes_with_main.filter(
                recipe_ingredients__ingredient__id__in=ingredient_ids
            ).annotate(
                matched_ingredients=Count('recipe_ingredients__ingredient__id',
                                          filter=Q(recipe_ingredients__ingredient__id__in=ingredient_ids),
                                          distinct=True)
            ).filter(matched_ingredients=len(ingredient_ids)).distinct()

            recipes_with_some_ingredients = recipes_with_main.filter(
                recipe_ingredients__ingredient__id__in=ingredient_ids
            ).annotate(
                matched_ingredients=Count('recipe_ingredients__ingredient__id',
                                          filter=Q(recipe_ingredients__ingredient__id__in=ingredient_ids),
                                          distinct=True)
            ).exclude(id__in=recipes_with_all_ingredients.values('id')).distinct().order_by('-matched_ingredients')

            for recipe in recipes_with_some_ingredients:
                missing_ingredients = list(set(ingredient_ids) - set(
                    recipe.recipe_ingredients.filter(ingredient__id__in=ingredient_ids).values_list('ingredient_id',
                                                                                                    flat=True)
                ))
                missing_ingredients_details = Ingredient.objects.filter(id__in=missing_ingredients)
                missing_ingredients_serialized = IngredientSerializer(missing_ingredients_details, many=True).data
                recipe.missing_ingredients = missing_ingredients_serialized
                recipe.missing_ingredients_count = missing_ingredients_details.count()
        else:
            recipes_with_all_ingredients = recipes_with_main
            recipes_with_some_ingredients = []

        serializer_all = SelectionRecipeSerializer(recipes_with_all_ingredients, many=True,
                                                   context={'request': request})
        serializer_some = SelectionRecipeSerializer(recipes_with_some_ingredients, many=True,
                                                    context={'request': request})

        return Response({
            'all_ingredients': serializer_all.data,
            'some_ingredients': serializer_some.data
        })

    @swagger_auto_schema(**recipe_create)
    def create(self, request, *args, **kwargs):
        data = request.data

        if isinstance(data, QueryDict):
            data = data.dict()
            for key in data:
                if key == 'tools' and isinstance(key, str):
                    data[key] = list(map(int, data[key].split(',')))
                elif key == 'ingredients' and isinstance(key, str):
                    ingredients_json = f'[{data["ingredients"]}]'
                    data[key] = json.loads(ingredients_json)
                elif key == 'isEnabled' and isinstance(key, str):
                    data[key] = bool(data[key])
                elif key == 'user' and isinstance(key, str):
                    data[key] = int(data[key])
                elif key == 'instruction' and isinstance(data[key], str):
                    clean_instruction = data[key].replace('\t', '').replace('\n', '')
                    data[key] = json.loads(clean_instruction)
                elif key == 'photo':
                    pass
                else:
                    data[key] = data[key].replace('"', '')

        serializer = CreateRecipeSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        return Response(RecipeDetailSerializer(recipe, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(**recipe_retrieve)
    def retrieve(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = RecipeDetailSerializer(recipe, context={'request': request})
        return Response(serializer.data)


class ClaimViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsActiveUser]

    def create(self, request, *args, **kwargs):
        data = request.data
        recipe_id = data.get('recipe_id')
        user = request.user

        if not recipe_id:
            return Response({"detail": "No recipe_id provided."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_anonymous:
            return Response({"detail": "User is anonymous."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"detail": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        if Claim.objects.filter(
                content_type=ContentType.objects.get_for_model(recipe),
                object_id=recipe.id,
                user=user
        ).exists():
            return Response({'detail': 'Claim already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        сlaim_obj = Claim.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(recipe),
            object_id=recipe.id,
            content_object=recipe
        )

        if сlaim_obj:
            try:
                cost = Config.objects.get(code='create_recipe')
                cost = int(cost.value)
            except Config.DoesNotExist:
                cost = 100

            Point.objects.create(user=user, text='Приготовил рецепт', points=cost, charge=False)

        serializer = self.get_serializer(сlaim_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
