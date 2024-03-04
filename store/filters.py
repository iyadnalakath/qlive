import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Teachers


# class TeacherFilter(django_filters.FilterSet):
#     has_roll_no = filters.BooleanFilter(
#         method='filter_has_roll_no',
#         label='Has Roll No',
#     )

#     experience = filters.NumberFilter(
#         method='filter_experience',
#         label='Experience',
#     )

#     def filter_has_roll_no(self, queryset, name, value):
#         if value:
#             # Filter teachers with roll numbers
#             return queryset.filter(roll_no__isnull=False)
#         else:
#             # Filter teachers without roll numbers
#             return queryset.exclude(roll_no__isnull=False)
        

#     def filter_experience(self, queryset, name, value):
#         # Filter teachers with experience greater than or equal to the provided value
#         return queryset.filter(experience__gte=value)

#     class Meta:
#         model = Teachers
#         fields = ['subject', 'experience', 'english_fluency', 'has_roll_no']



class TeacherFilter(django_filters.FilterSet):
    has_roll_no = filters.BooleanFilter(
        method='filter_has_roll_no',
        label='Has Roll No',
    )

    experience = filters.NumberFilter(
        method='filter_experience',
        label='Experience',
    )

    grade = filters.CharFilter(
        method='filter_grade',
        label='Grade',
    )
    def filter_has_roll_no(self, queryset, name, value):
        if value:
            # Filter teachers with non-empty roll numbers
            return queryset.exclude(roll_no__exact="")
        else:
            # Filter teachers with empty roll numbers
            return queryset.filter(roll_no__exact="")

    def filter_experience(self, queryset, name, value):
        # Filter teachers with experience greater than or equal to the provided value
        return queryset.filter(experience__gte=value)

    def filter_grade(self, queryset, name, value):
        # Filter teachers based on the associated grade
        return queryset.filter(Q(remunerations__grade=value))

    class Meta:
        model = Teachers
        fields = ['subject', 'experience', 'english_fluency', 'has_roll_no', 'grade']
