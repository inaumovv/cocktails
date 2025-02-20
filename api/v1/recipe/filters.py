from django.db.models import Q, BooleanField, Case, When, Value, Count
from django_filters import rest_framework as filters
from apps.recipe.models import Recipe


class RecipeFilterSet(filters.FilterSet):
    q = filters.CharFilter(method='filter_q')
    ingredients = filters.CharFilter(method='filter_ingredients')
    tools = filters.CharFilter(method='filter_tools')
    ordering = filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('video_url', 'video_url'),
            ('popularity', 'popularity'),
        ),
        field_labels={
            'title': 'Recipe title',
            'video_url': 'Video exists',
            'popularity': 'Popularity',
        }
    )

    @staticmethod
    def filter_q(queryset, name, value):
        if not value:
            return queryset

        value_list = value.split()
        q = Q()

        for word in value_list:
            q |= Q(title__icontains=word) | Q(recipe_ingredients__ingredient__name__icontains=word)

        if len(value_list) > 1:
            for i in range(len(value_list)):
                for j in range(i + 1, len(value_list)):
                    q |= (
                            (Q(title__icontains=value_list[i]) & Q(title__icontains=value_list[j])) |
                            (Q(recipe_ingredients__ingredient__name__icontains=value_list[i]) & Q(
                                recipe_ingredients__ingredient__name__icontains=value_list[j]))
                    )

        return queryset.filter(q).distinct()

    def filter_ingredients(self, queryset, name, value):
        if not value:
            return queryset

        try:
            ids = [int(v) for v in value.replace('-', ',').split(',')]
        except ValueError:
            return queryset.none()

        return queryset.filter(recipe_ingredients__ingredient__id__in=ids).distinct()

    def filter_tools(self, queryset, name, value):
        if not value:
            return queryset

        try:
            ids = [int(v) for v in value.replace('-', ',').split(',')]
        except ValueError:
            return queryset.none()

        return queryset.filter(tools__id__in=ids).distinct()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def filter_queryset(self, queryset):
        queryset = queryset.annotate(popularity=Count('favorited_by'))
        return super().filter_queryset(queryset)

    class Meta:
        model = Recipe
        fields = ['q', 'ingredients', 'tools', 'ordering']
