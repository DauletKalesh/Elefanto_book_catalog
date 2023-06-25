import django_filters as filters
from main.models import Book

class BookFilterSet(filters.FilterSet):

    genre = filters.CharFilter(field_name='genres__name', lookup_expr='exact')
    author_first_name = filters.CharFilter(
        field_name='authors__first_name', lookup_expr='exact')
    author_last_name = filters.CharFilter(
        field_name='authors__last_name', lookup_expr='exact')
    
    max_publication_year = filters.NumberFilter(
        field_name='publication_date__year', lookup_expr='gte')
    min_publication_year = filters.NumberFilter(
        field_name='publication_date__year', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ('genre', 'author_first_name', 'author_last_name', 'max_publication_year',
                  'min_publication_year')