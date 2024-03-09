from .models import Posts
from django_filters import FilterSet, CharFilter
from django_filters import rest_framework as filters


class PostFilter(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    blog_post = filters.CharFilter(lookup_expr='icontains')
    tag = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Posts
        fields = ['title', 'blog_post', 'tag']
