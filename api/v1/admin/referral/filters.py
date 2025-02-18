import django_filters
from django.db.models import Q

from apps.user.models import Referral


class ReferralFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Referral
        fields = []

    def filter_search(self, queryset, name, value):
        query = Q()

        if value.isdigit():
            query |= Q(user_id=value)

        return queryset.filter(query)