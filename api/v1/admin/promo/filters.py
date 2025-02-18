import django_filters
from django.db.models import Q

from apps.goods.models import Promo, PurchasedPromo


class PromoFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Promo
        fields = []

    def filter_search(self, queryset, name, value):
        query = Q()

        query |= Q(name__icontains=value)

        query |= Q(description__icontains=value)

        return queryset.filter(query)