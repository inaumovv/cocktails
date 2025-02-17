import django_filters
from django.db.models import Q

from apps.user.models import User


class ProfileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = User
        fields = []

    def filter_search(self, queryset, name, value):
        query = Q()

        query |= Q(first_name__icontains=value)

        query |= Q(last_name__icontains=value)

        if any(char.isdigit() for char in value):
            query |= Q(phone__icontains=value)

        query |= Q(email__icontains=value)

        if value.isdigit():
            query |= Q(id=value)

        return queryset.filter(query)
