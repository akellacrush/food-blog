from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticleList.as_view(), name='index'),
    path('category/<int:category_id>/', ArticleListByCategory.as_view(), name='category'),
    path('add/', NewArticle.as_view(), name='add'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('search/', SearchResults.as_view(), name='search'),
    path('about_dev/', about_dev, name='about_dev'),
    path('user_register/', user_register, name='user_register'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('add_comment/<int:pk>', save_comment, name='save_comment'),
    path('add_or_delete_mark/<int:article_id>/<str:action>/', add_or_delete_mark, name='mark')
]
