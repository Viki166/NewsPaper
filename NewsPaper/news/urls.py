from django.urls import path
from .views import PostsList, PostDetail


urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]