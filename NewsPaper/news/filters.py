from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'date_of_creation_post': ['gt'],
                  'author': ['exact'],
                  }
