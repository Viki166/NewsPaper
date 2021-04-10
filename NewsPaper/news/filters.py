from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля по которым будет фильтроваться (т.е. подбираться) информация о новостях
    class Meta:
        model = Post
        fields = {'date_of_creation_post': ['gt'],  #количество новостей должно быть больше или равно тому, что указал
                  'author': ['exact'],
                  }  # поля которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)


