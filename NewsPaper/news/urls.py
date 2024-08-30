from django.urls import path
# Импортируем созданное нами представление
from .views import (NewsListView, NewsDetail, Search, NewsCreate, ArticlesCreate, NewsEdit,
                    ArticlesEdit, NewsDelete, ArticlesDelete, CategoryList, CategorySubscribe)


urlpatterns = [
   # path — означает путь.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('', NewsListView.as_view(), name='home'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('news/search/', Search.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('news/category/', CategoryList.as_view(), name='category_list'),
    path('news/category/<int:pk>/subscribe/', CategorySubscribe.as_view(), name='category_subscribe'),
]