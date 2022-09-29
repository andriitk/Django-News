from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', cache_page(60)(HomeView.as_view()), name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', NewsCategory.as_view(), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add_news/', add_news, name='add_news'),
    path('news/add_news/', AddNews.as_view(), name='add_news'),
    path('news/feedback/', feedback, name='feedback'),
]
