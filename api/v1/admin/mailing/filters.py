import django_filters
from django.db.models import Q

from apps.common.models import Ads, Mailing


class MailingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Mailing
        fields = []

    def filter_search(self, queryset, name, value):
        query = Q()

        query |= Q(title__icontains=value)

        query |= Q(description__icontains=value)

        query |= Q(title_eng__icontains=value)

        query |= Q(description_eng__icontains=value)

        return queryset.filter(query)
