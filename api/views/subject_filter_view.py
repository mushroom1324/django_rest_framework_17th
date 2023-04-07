from django_filters.rest_framework import FilterSet, filters
from subject.models import Subject


class SubjectFilter(FilterSet):
    subject_name = filters.CharFilter(lookup_expr='icontains', label='과목명')
    professor_name = filters.CharFilter(lookup_expr='icontains', label='교수명')
    is_cyber = filters.BooleanFilter(method='is_cyber_filter', label='비대면 여부')

    class Meta:
        model = Subject
        fields = ['subject_name', 'professor_name', 'is_cyber']

    def is_cyber_filter(self, queryset, name, value):
        return queryset.filter(is_cyber=True) if value else queryset.filter(is_cyber=False)