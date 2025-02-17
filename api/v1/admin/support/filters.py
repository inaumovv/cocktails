import django_filters
from django.db.models import Q

from apps.channel.models import Ticket


class TicketFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Ticket
        fields = []

    def filter_search(self, queryset, name, value):
        query = Q()

        if any(char.isdigit() for char in value):
            query |= Q(user__phone__icontains=value)

        query |= Q(user__email__icontains=value)

        if value.isdigit():
            query |= Q(id=value)
            query |= Q(user_id=value)

        return queryset.filter(query)
