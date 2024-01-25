import django_filters
from django_filters import rest_framework as filters
from .models import Teachers

class TeacherFilter(django_filters.FilterSet):
    has_roll_no = filters.BooleanFilter(
        method='filter_has_roll_no',
        label='Has Roll No',
    )

    def filter_has_roll_no(self, queryset, name, value):
        if value:
            # Filter teachers with roll numbers
            return queryset.filter(roll_no__isnull=False)
        else:
            # Filter teachers without roll numbers
            return queryset.exclude(roll_no__isnull=False)

    class Meta:
        model = Teachers
        fields = ['subject', 'experience', 'english_fluency', 'has_roll_no']
