from django.forms import DateInput
from django_filters import FilterSet, DateFilter, CharFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    time = DateFilter(lookup_expr='gt', label='Опубликовано после ', widget=DateInput(format='%d.%m.%Y', attrs={'type': 'date'}))
    postAuthor__authorUser__username = CharFilter(lookup_expr='iexact', label='Имя автора')
    class Meta:
        model = Post
        fields = ['header', 'time', 'postAuthor__authorUser__username']
