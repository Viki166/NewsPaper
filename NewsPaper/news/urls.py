from django.urls import path
from .views import *


urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', SearchList.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    #path('upgrade/', upgrade_me, name='upgrade')
]