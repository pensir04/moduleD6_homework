from django.urls import path, include
from .views import Posts, PostSearch, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, subscribe_me
from .forms import upgrade_me

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', Posts.as_view()),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('search/', PostSearch.as_view()), # Ссылка на поиск
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Ссылка на детали поста
    path('create/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание поста
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),  # Ссылка на редактирование поста
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),  # Ссылка на удаление поста
    path('upgrade/', upgrade_me, name='upgrade'),
    path('posts/accounts/', include('allauth.urls')),
    path('<int:pk>/subscribe/', subscribe_me, name = 'subscribe'),
]
